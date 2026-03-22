import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, List, ListItem, ListItemText, Card, CardContent, Button, TextField, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';
import api from '../api';
import { useI18n } from '../i18n';

const ProfessorDashboard: React.FC = () => {
  const [courses, setCourses] = useState<any[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<any>(null);
  const [assignments, setAssignments] = useState<any[]>([]);

  // Create Course Modal
  const [openCourseModal, setOpenCourseModal] = useState(false);
  const [newCourseTitle, setNewCourseTitle] = useState('');
  const [newCourseDesc, setNewCourseDesc] = useState('');

  // Create Assignment Modal
  const [openAssignmentModal, setOpenAssignmentModal] = useState(false);
  const [newAssignmentTitle, setNewAssignmentTitle] = useState('');
  const [newAssignmentDesc, setNewAssignmentDesc] = useState('');

  // Invite Student Modal
  const [openInviteModal, setOpenInviteModal] = useState(false);
  const [inviteEmail, setInviteEmail] = useState('');
  const { t } = useI18n();

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const res = await api.get('/courses');
      setCourses(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchAssignments = async (courseId: number) => {
    try {
      const res = await api.get(`/courses/${courseId}/assignments`);
      setAssignments(res.data);
      setSelectedCourse(courseId);
    } catch (err) {
      console.error(err);
    }
  };

  const handleCreateCourse = async () => {
    try {
      await api.post('/courses', { title: newCourseTitle, description: newCourseDesc });
      setOpenCourseModal(false);
      fetchCourses();
      setNewCourseTitle('');
      setNewCourseDesc('');
    } catch (err) {
      console.error(err);
    }
  };

  const handleCreateAssignment = async () => {
    if (!selectedCourse) return;
    try {
      await api.post(`/courses/${selectedCourse}/assignments`, {
        title: newAssignmentTitle,
        description: newAssignmentDesc,
        docker_env: 'basic'
      });
      setOpenAssignmentModal(false);
      fetchAssignments(selectedCourse);
      setNewAssignmentTitle('');
      setNewAssignmentDesc('');
    } catch (err) {
      console.error(err);
    }
  };

  const handleInviteStudent = async () => {
    try {
      await api.post('/users/invite', { email: inviteEmail });
      setOpenInviteModal(false);
      setInviteEmail('');
      alert(t('inviteSuccess'));
    } catch (err) {
      console.error(err);
      alert(t('inviteFail'));
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>{t('professorDashboard')}</Typography>

      <Box sx={{ display: 'flex', gap: 4 }}>
        {/* Left column: Courses */}
        <Box sx={{ width: '30%' }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">{t('myCourses')}</Typography>
            <Button variant="outlined" size="small" onClick={() => setOpenCourseModal(true)}>+</Button>
          </Box>
          <List>
            {courses.map(course => (
              <ListItem component="button" key={course.id} onClick={() => fetchAssignments(course.id)}>
                <ListItemText primary={course.title} secondary={course.description} />
              </ListItem>
            ))}
          </List>

          <Button variant="contained" sx={{ mt: 2 }} fullWidth onClick={() => setOpenInviteModal(true)}>
            {t('inviteStudent')}
          </Button>
        </Box>

        {/* Right column: Assignments */}
        <Box sx={{ width: '70%' }}>
          {selectedCourse ? (
            <>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">{t('assignments')}</Typography>
                <Button variant="contained" size="small" onClick={() => setOpenAssignmentModal(true)}>{t('newAssignment')}</Button>
              </Box>

              {assignments.map(assignment => (
                <Card key={assignment.id} sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="h6">{assignment.title}</Typography>
                    <Typography variant="body2">{assignment.description}</Typography>
                    <Typography variant="caption" color="text.secondary">{t('dockerEnv')} {assignment.docker_env}</Typography>

                    <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                       <Button variant="outlined" size="small">{t('manageRubric')}</Button>
                       <Button variant="outlined" size="small">{t('uploadTestSet')}</Button>
                       <Button variant="outlined" size="small">{t('viewSubmissions')}</Button>
                    </Box>
                  </CardContent>
                </Card>
              ))}
            </>
          ) : (
            <Typography variant="body1" color="text.secondary">{t('selectCourse')}</Typography>
          )}
        </Box>
      </Box>

      {/* Course Modal */}
      <Dialog open={openCourseModal} onClose={() => setOpenCourseModal(false)}>
        <DialogTitle>{t('createCourseTitle')}</DialogTitle>
        <DialogContent>
          <TextField autoFocus margin="dense" label={t('courseTitle')} fullWidth value={newCourseTitle} onChange={(e) => setNewCourseTitle(e.target.value)} />
          <TextField margin="dense" label={t('description')} fullWidth multiline rows={3} value={newCourseDesc} onChange={(e) => setNewCourseDesc(e.target.value)} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenCourseModal(false)}>{t('cancel')}</Button>
          <Button onClick={handleCreateCourse}>{t('create')}</Button>
        </DialogActions>
      </Dialog>

      {/* Assignment Modal */}
      <Dialog open={openAssignmentModal} onClose={() => setOpenAssignmentModal(false)}>
        <DialogTitle>{t('createAssignmentTitle')}</DialogTitle>
        <DialogContent>
          <TextField autoFocus margin="dense" label={t('assignmentTitle')} fullWidth value={newAssignmentTitle} onChange={(e) => setNewAssignmentTitle(e.target.value)} />
          <TextField margin="dense" label={t('description')} fullWidth multiline rows={3} value={newAssignmentDesc} onChange={(e) => setNewAssignmentDesc(e.target.value)} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAssignmentModal(false)}>{t('cancel')}</Button>
          <Button onClick={handleCreateAssignment}>{t('create')}</Button>
        </DialogActions>
      </Dialog>

       {/* Invite Student Modal */}
       <Dialog open={openInviteModal} onClose={() => setOpenInviteModal(false)}>
        <DialogTitle>{t('inviteStudentTitle')}</DialogTitle>
        <DialogContent>
          <TextField autoFocus margin="dense" label={t('studentEmail')} type="email" fullWidth value={inviteEmail} onChange={(e) => setInviteEmail(e.target.value)} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenInviteModal(false)}>{t('cancel')}</Button>
          <Button onClick={handleInviteStudent} color="primary" variant="contained">{t('sendInvite')}</Button>
        </DialogActions>
      </Dialog>

    </Container>
  );
};

export default ProfessorDashboard;
