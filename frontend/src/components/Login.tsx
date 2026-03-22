import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api';
import { useAuth } from '../AuthContext';
import { useI18n } from '../i18n';
import { Container, Typography, TextField, Button, Box, Alert } from '@mui/material';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth();
  const { t } = useI18n();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const params = new URLSearchParams();
      params.append('username', email);
      params.append('password', password);

      const res = await api.post('/login/access-token', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });

      const token = res.data.access_token;

      const userRes = await api.get('/users/me', {
        headers: { Authorization: `Bearer ${token}` }
      });

      login(token, userRes.data);

      if (userRes.data.role === 'professor') {
        navigate('/professor');
      } else {
        navigate('/student');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || t('loginFailed'));
    }
  };

  return (
    <Container maxWidth="xs">
      <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography component="h1" variant="h5">
          {t('signIn')}
        </Typography>
        {error && <Alert severity="error" sx={{ width: '100%', mt: 2 }}>{error}</Alert>}
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label={t('emailAddress')}
            name="email"
            autoComplete="email"
            autoFocus
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label={t('password')}
            type="password"
            id="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            {t('signInBtn')}
          </Button>
          <Box sx={{ display: 'flex', justifyContent: 'center' }}>
              <Link to="/register" style={{textDecoration: 'none', color: '#1976d2'}}>
                {t('noAccount')}
              </Link>
          </Box>
        </Box>
      </Box>
    </Container>
  );
};

export default Login;
