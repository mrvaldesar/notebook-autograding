export const translations = {
  en: {
    // Login
    signIn: "Sign in",
    emailAddress: "Email Address",
    password: "Password",
    signInBtn: "Sign In",
    noAccount: "Don't have an account? Register with token",
    loginFailed: "Login failed",

    // Register
    studentRegistration: "Student Registration",
    invitationToken: "Invitation Token",
    fullName: "Full Name",
    studentId: "Student ID (Carnet)",
    registerBtn: "Register",
    registrationFailed: "Registration failed",

    // Professor Dashboard
    professorDashboard: "Professor Dashboard",
    myCourses: "My Courses",
    inviteStudent: "Invite Student",
    assignments: "Assignments",
    newAssignment: "New Assignment",
    dockerEnv: "Docker Env:",
    manageRubric: "Manage Rubric",
    uploadTestSet: "Upload Test Set",
    viewSubmissions: "View Submissions",
    selectCourse: "Select a course to view assignments",

    createCourseTitle: "Create New Course",
    courseTitle: "Course Title",
    description: "Description",
    cancel: "Cancel",
    create: "Create",

    createAssignmentTitle: "Create New Assignment",
    assignmentTitle: "Assignment Title",

    inviteStudentTitle: "Invite Student to Platform",
    studentEmail: "Student Email",
    sendInvite: "Send Invite",
    inviteSuccess: "Invitation sent successfully",
    inviteFail: "Failed to send invitation",

    // Student Dashboard
    studentDashboard: "Student Dashboard",
    due: "Due:",
    submitNotebook: "Submit Notebook",
    submitSuccess: "Notebook submitted successfully!",
    submitFail: "Submission failed.",
  },
  "es-GT": {
    // Login
    signIn: "Iniciar sesión",
    emailAddress: "Correo Electrónico",
    password: "Contraseña",
    signInBtn: "Ingresar",
    noAccount: "¿No tienes una cuenta? Regístrate con un token",
    loginFailed: "Error al iniciar sesión",

    // Register
    studentRegistration: "Registro de Estudiante",
    invitationToken: "Token de Invitación",
    fullName: "Nombre Completo",
    studentId: "Carné de Estudiante",
    registerBtn: "Registrarse",
    registrationFailed: "Error en el registro",

    // Professor Dashboard
    professorDashboard: "Panel de Profesor",
    myCourses: "Mis Cursos",
    inviteStudent: "Invitar Estudiante",
    assignments: "Tareas",
    newAssignment: "Nueva Tarea",
    dockerEnv: "Entorno Docker:",
    manageRubric: "Gestionar Rúbrica",
    uploadTestSet: "Subir Conjunto de Pruebas",
    viewSubmissions: "Ver Entregas",
    selectCourse: "Selecciona un curso para ver las tareas",

    createCourseTitle: "Crear Nuevo Curso",
    courseTitle: "Título del Curso",
    description: "Descripción",
    cancel: "Cancelar",
    create: "Crear",

    createAssignmentTitle: "Crear Nueva Tarea",
    assignmentTitle: "Título de la Tarea",

    inviteStudentTitle: "Invitar Estudiante a la Plataforma",
    studentEmail: "Correo del Estudiante",
    sendInvite: "Enviar Invitación",
    inviteSuccess: "Invitación enviada exitosamente",
    inviteFail: "Error al enviar la invitación",

    // Student Dashboard
    studentDashboard: "Panel de Estudiante",
    due: "Vence:",
    submitNotebook: "Entregar Notebook",
    submitSuccess: "¡Notebook entregado exitosamente!",
    submitFail: "Error en la entrega.",
  }
};

export type Language = "en" | "es-GT";
export type TranslationKey = keyof typeof translations["en"];
