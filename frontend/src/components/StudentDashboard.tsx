import React, { useState, useEffect } from 'react';
import api from '../api';
import { Container, Typography, Card, CardContent, Button, Box, List, ListItem, ListItemText, TextField } from '@mui/material';

const StudentDashboard: React.FC = () => {
  const [courses, setCourses] = useState<any[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<any>(null);
  const [assignments, setAssignments] = useState<any[]>([]);
  const [file, setFile] = useState<File | null>(null);

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

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (assignmentId: number) => {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    try {
      await api.post(`/submissions/assignments/${assignmentId}/submit`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      alert('Notebook submitted successfully!');
      setFile(null);
    } catch (err) {
      console.error(err);
      alert('Submission failed.');
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Student Dashboard</Typography>

      <Box sx={{ display: 'flex', gap: 2 }}>
        <Box sx={{ width: '30%' }}>
          <Typography variant="h6">My Courses</Typography>
          <List>
            {courses.map(course => (
              <ListItem button key={course.id} onClick={() => fetchAssignments(course.id)}>
                <ListItemText primary={course.title} />
              </ListItem>
            ))}
          </List>
        </Box>

        <Box sx={{ width: '70%' }}>
          {selectedCourse && (
            <>
              <Typography variant="h6">Assignments</Typography>
              {assignments.map(assignment => (
                <Card key={assignment.id} sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="h6">{assignment.title}</Typography>
                    <Typography variant="body2" color="text.secondary">Due: {assignment.due_date || 'N/A'}</Typography>
                    <Typography variant="body2">{assignment.description}</Typography>

                    <Box sx={{ mt: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
                      <TextField type="file" onChange={handleFileChange} size="small" />
                      <Button variant="contained" color="primary" onClick={() => handleSubmit(assignment.id)} disabled={!file}>
                        Submit Notebook
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              ))}
            </>
          )}
        </Box>
      </Box>
    </Container>
  );
};

export default StudentDashboard;
