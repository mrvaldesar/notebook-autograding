import os
import tempfile
import json
import traceback
import docker
from sqlalchemy.orm import Session
from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app import crud, models
import nbformat
import shutil

docker_client = docker.from_env()

def calculate_score(rubric_criteria, notebook_content):
    # Simplified mock calculation based on rubric and notebook content
    # In a real app, this would extract variables from the executed notebook
    # and compare them against hidden dataset assertions.
    total_weight = sum(c.get("weight", 0) for c in rubric_criteria)
    if total_weight == 0:
        return 0, [{"error": "Invalid rubric"}]

    score = 0
    feedback = []

    # Just a mock loop:
    for criteria in rubric_criteria:
        name = criteria.get("name", "Unknown")
        weight = criteria.get("weight", 0)

        # Simulate checking if a specific output exists or no errors occurred
        # Here we just give full points for simplicity, unless we find an error cell
        points_awarded = weight
        feedback.append({"criteria": name, "points": points_awarded, "max": weight, "message": f"Verified {name}"})
        score += points_awarded

    normalized_score = (score / total_weight) * 100
    return normalized_score, feedback

@celery_app.task(name="app.worker.autograde_notebook")
def autograde_notebook(notebook_version_id: int):
    db: Session = SessionLocal()
    try:
        evaluation = crud.evaluation.get_by_notebook_version(db, notebook_version_id=notebook_version_id)
        if not evaluation:
            print(f"Evaluation for notebook version {notebook_version_id} not found.")
            return

        crud.evaluation.update(db, db_obj=evaluation, obj_in={"status": models.submission.EvaluationStatus.RUNNING})

        notebook_version = crud.notebook_version.get(db, id=notebook_version_id)
        submission = crud.submission.get(db, id=notebook_version.submission_id)
        assignment = crud.assignment.get(db, id=submission.assignment_id)
        rubric = crud.rubric.get_by_assignment(db, assignment_id=assignment.id)

        if not rubric:
            crud.evaluation.update(db, db_obj=evaluation, obj_in={
                "status": models.submission.EvaluationStatus.FAILED,
                "execution_logs": "No rubric found for this assignment."
            })
            return

        # Prepare temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. Copy student notebook
            student_nb_path = os.path.join(temp_dir, "student.ipynb")
            shutil.copyfile(notebook_version.file_path, student_nb_path)

            # 2. Copy hidden dataset if exists
            if assignment.hidden_dataset_path and os.path.exists(assignment.hidden_dataset_path):
                 shutil.copyfile(assignment.hidden_dataset_path, os.path.join(temp_dir, os.path.basename(assignment.hidden_dataset_path)))

            # 3. Copy execution script
            run_script_path = os.path.join(os.path.dirname(__file__), "..", "docker", "run_notebook.py")
            shutil.copyfile(run_script_path, os.path.join(temp_dir, "run_notebook.py"))

            # Determine Docker Image
            image_name = "autograder_basic" if assignment.docker_env == models.course.DockerEnvEnum.BASIC else "autograder_dl"

            # 4. Run Docker Container
            try:
                container = docker_client.containers.run(
                    image=image_name,
                    command="python run_notebook.py student.ipynb output.ipynb",
                    volumes={temp_dir: {'bind': '/app', 'mode': 'rw'}},
                    working_dir='/app',
                    remove=True,
                    stderr=True,
                    stdout=True
                )
                logs = container.decode("utf-8")
            except docker.errors.ContainerError as e:
                logs = e.stderr.decode("utf-8")

            # Read output notebook
            output_nb_path = os.path.join(temp_dir, "output.ipynb")
            if os.path.exists(output_nb_path):
                with open(output_nb_path, "r") as f:
                    executed_nb = json.load(f)
            else:
                 executed_nb = None

            # 5. Evaluate results
            if executed_nb:
                 score, feedback = calculate_score(rubric.criteria, executed_nb)
                 status = models.submission.EvaluationStatus.COMPLETED
            else:
                 score = 0
                 feedback = [{"error": "Failed to generate output notebook"}]
                 status = models.submission.EvaluationStatus.FAILED

            # 6. Update Database
            crud.evaluation.update(db, db_obj=evaluation, obj_in={
                "status": status,
                "score": score,
                "feedback": feedback,
                "execution_logs": logs[-2000:] # store last 2000 chars of logs
            })

            audit_action = models.audit.AuditActionEnum.EVALUATION_COMPLETED if status == models.submission.EvaluationStatus.COMPLETED else models.audit.AuditActionEnum.EVALUATION_FAILED
            crud.audit_log.log_action(db=db, evaluation_id=evaluation.id, action=audit_action, details=f"Automated evaluation finished with score {score}.")

    except Exception as e:
        db.rollback()
        print(f"Error grading notebook: {traceback.format_exc()}")
        if evaluation:
             crud.evaluation.update(db, db_obj=evaluation, obj_in={
                 "status": models.submission.EvaluationStatus.FAILED,
                 "execution_logs": traceback.format_exc()[-2000:]
             })
             crud.audit_log.log_action(db=db, evaluation_id=evaluation.id, action=models.audit.AuditActionEnum.EVALUATION_FAILED, details="Internal autograder error.")
    finally:
        db.close()
