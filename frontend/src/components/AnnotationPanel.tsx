import {
  Box,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  Typography,
} from '@mui/material'
import { Delete, Visibility, VisibilityOff, Lock } from '@mui/icons-material'
import { useAnnotationStore } from '../store/annotationStore'
import { useQuery } from '@tanstack/react-query'
import api from '../api/client'
import { LabelSchema } from '../types/annotation'

interface AnnotationPanelProps {
  wsiId: number
}

export function AnnotationPanel({}: AnnotationPanelProps) {
  const { annotations, selectedAnnotation, setSelectedAnnotation, currentLabel, setCurrentLabel } =
    useAnnotationStore()

  const { data: labelSchema } = useQuery<LabelSchema>({
    queryKey: ['label-schema-default'],
    queryFn: async () => {
      const response = await api.get('/labels/default')
      return response.data
    },
  })

  const labelClasses = labelSchema?.schema_definition?.classes || []

  return (
    <Box>
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel>Current Label</InputLabel>
        <Select
          value={currentLabel}
          onChange={(e) => setCurrentLabel(e.target.value)}
          label="Current Label"
        >
          {labelClasses.map((cls) => (
            <MenuItem key={cls.name} value={cls.name}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Box
                  sx={{
                    width: 16,
                    height: 16,
                    bgcolor: cls.color,
                    borderRadius: '50%',
                  }}
                />
                {cls.name}
              </Box>
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <Typography variant="subtitle2" sx={{ mb: 1 }}>
        Annotations ({annotations.length})
      </Typography>

      <List>
        {annotations.map((ann) => (
          <ListItem
            key={ann.id}
            selected={selectedAnnotation?.id === ann.id}
            onClick={() => setSelectedAnnotation(ann)}
            secondaryAction={
              <Box>
                <IconButton
                  size="small"
                  onClick={() => {
                    // Toggle visibility
                  }}
                >
                  {ann.is_visible ? <Visibility /> : <VisibilityOff />}
                </IconButton>
                <IconButton
                  size="small"
                  onClick={() => {
                    // Delete annotation
                  }}
                >
                  <Delete />
                </IconButton>
              </Box>
            }
          >
            <ListItemText
              primary={
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Chip
                    label={ann.label}
                    size="small"
                    sx={{
                      bgcolor: ann.color || '#FF0000',
                      color: 'white',
                      fontSize: '0.7rem',
                    }}
                  />
                  {ann.is_locked && <Lock fontSize="small" />}
                </Box>
              }
              secondary={ann.description || `${ann.geometry_type}`}
            />
          </ListItem>
        ))}
      </List>
    </Box>
  )
}
