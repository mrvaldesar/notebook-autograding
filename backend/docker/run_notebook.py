import sys
import json
import traceback
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError

def run_notebook(notebook_path, output_path):
    try:
        with open(notebook_path) as f:
            nb = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

        try:
            ep.preprocess(nb, {'metadata': {'path': './'}})
            with open(output_path, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)
            print(json.dumps({"status": "success", "message": "Execution completed successfully"}))
        except CellExecutionError as e:
             with open(output_path, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)
             print(json.dumps({"status": "failed", "error": str(e), "message": "Cell execution failed"}))

    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e), "traceback": traceback.format_exc()}))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run_notebook.py <input.ipynb> <output.ipynb>")
        sys.exit(1)

    run_notebook(sys.argv[1], sys.argv[2])
