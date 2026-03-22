import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import ProfessorDashboard from './components/ProfessorDashboard';
import StudentDashboard from './components/StudentDashboard';
import { AuthProvider, useAuth } from './AuthContext';
import { I18nProvider, useI18n } from './i18n';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { AppBar, Toolbar, Button, Box } from '@mui/material';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f4f6f8',
    },
  },
});

const PrivateRoute: React.FC<{ children: React.ReactElement, role: 'professor' | 'student' }> = ({ children, role }) => {
  const { user, isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  if (user?.role !== role) {
    return <Navigate to={`/${user?.role}`} />;
  }

  return children;
};

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route path="/professor" element={
        <PrivateRoute role="professor">
          <ProfessorDashboard />
        </PrivateRoute>
      } />

      <Route path="/student" element={
        <PrivateRoute role="student">
          <StudentDashboard />
        </PrivateRoute>
      } />
    </Routes>
  );
};

const LanguageSwitcher: React.FC = () => {
  const { language, setLanguage } = useI18n();
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" color="transparent" elevation={0}>
        <Toolbar sx={{ justifyContent: 'flex-end' }}>
          <Button
            color="inherit"
            onClick={() => setLanguage(language === 'en' ? 'es-GT' : 'en')}
          >
            {language === 'en' ? 'Español' : 'English'}
          </Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
};

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <I18nProvider>
        <AuthProvider>
          <Router>
            <LanguageSwitcher />
            <AppRoutes />
          </Router>
        </AuthProvider>
      </I18nProvider>
    </ThemeProvider>
  );
};

export default App;
