import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import {
  Box,
  Container,
  Typography,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
} from '@mui/material'
import { Visibility, Upload, Logout } from '@mui/icons-material'
import api from '../api/client'
import { authApi } from '../api/auth'
import { useAuthStore } from '../store/authStore'

interface WSIFile {
  id: number
  filename: string
  original_filename: string
  width: number | null
  height: number | null
  magnification: number | null
  created_at: string
}

export default function Dashboard() {
  const navigate = useNavigate()
  const { user } = useAuthStore()

  const { data: wsiFiles, isLoading } = useQuery<WSIFile[]>({
    queryKey: ['wsi-files'],
    queryFn: async () => {
      const response = await api.get('/wsi/')
      return response.data
    },
  })

  const handleView = (wsiId: number) => {
    navigate(`/viewer/${wsiId}`)
  }

  const handleLogout = () => {
    authApi.logout()
    navigate('/login')
  }

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Box
        sx={{
          bgcolor: 'primary.main',
          color: 'white',
          p: 2,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <Typography variant="h5">Oral Cytology WSI Annotation Tool</Typography>
        <Box>
          <Typography variant="body2" sx={{ mr: 2, display: 'inline' }}>
            {user?.username} ({user?.role})
          </Typography>
          <IconButton color="inherit" onClick={handleLogout}>
            <Logout />
          </IconButton>
        </Box>
      </Box>

      <Container maxWidth="lg" sx={{ flex: 1, py: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h4">WSI Files</Typography>
          <Button variant="contained" startIcon={<Upload />}>
            Upload WSI
          </Button>
        </Box>

        {isLoading ? (
          <Typography>Loading...</Typography>
        ) : (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Filename</TableCell>
                  <TableCell>Dimensions</TableCell>
                  <TableCell>Magnification</TableCell>
                  <TableCell>Uploaded</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {wsiFiles?.map((file) => (
                  <TableRow key={file.id}>
                    <TableCell>{file.original_filename}</TableCell>
                    <TableCell>
                      {file.width && file.height
                        ? `${file.width} × ${file.height}`
                        : 'N/A'}
                    </TableCell>
                    <TableCell>
                      {file.magnification ? `${file.magnification}×` : 'N/A'}
                    </TableCell>
                    <TableCell>
                      {new Date(file.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      <IconButton
                        color="primary"
                        onClick={() => handleView(file.id)}
                      >
                        <Visibility />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Container>
    </Box>
  )
}
