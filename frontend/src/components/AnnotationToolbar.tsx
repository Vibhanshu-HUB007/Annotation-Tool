import {
  Box,
  Button,
  Menu,
  MenuItem,
  Tooltip,
  ToggleButton,
  ToggleButtonGroup,
} from '@mui/material'
import {
  Edit,
  CropFree,
  RadioButtonUnchecked,
  Delete,
  Save,
  Download,
} from '@mui/icons-material'
import { useState } from 'react'
import { useAnnotationStore } from '../store/annotationStore'

interface AnnotationToolbarProps {
  onSave: () => void
  onExport: (format: 'coco' | 'geojson' | 'csv') => void
}

export function AnnotationToolbar({ onSave, onExport }: AnnotationToolbarProps) {
  const { currentTool, setCurrentTool } = useAnnotationStore()
  const [exportMenuAnchor, setExportMenuAnchor] = useState<null | HTMLElement>(null)

  const handleToolChange = (
    _event: React.MouseEvent<HTMLElement>,
    newTool: string | null
  ) => {
    if (newTool !== null) {
      setCurrentTool(newTool as any)
    }
  }

  return (
    <Box
      sx={{
        position: 'absolute',
        top: 10,
        left: 10,
        zIndex: 1000,
        bgcolor: 'rgba(255, 255, 255, 0.9)',
        borderRadius: 1,
        p: 1,
        display: 'flex',
        gap: 1,
        alignItems: 'center',
      }}
    >
      <ToggleButtonGroup
        value={currentTool}
        exclusive
        onChange={handleToolChange}
        size="small"
      >
        <ToggleButton value="select">
          <Tooltip title="Select">
            <Edit />
          </Tooltip>
        </ToggleButton>
        <ToggleButton value="freehand">
          <Tooltip title="Freehand">
            <Edit />
          </Tooltip>
        </ToggleButton>
        <ToggleButton value="polygon">
          <Tooltip title="Polygon">
            <CropFree />
          </Tooltip>
        </ToggleButton>
        <ToggleButton value="rectangle">
          <Tooltip title="Rectangle">
            <CropFree />
          </Tooltip>
        </ToggleButton>
        <ToggleButton value="point">
          <Tooltip title="Point">
            <RadioButtonUnchecked />
          </Tooltip>
        </ToggleButton>
        <ToggleButton value="erase">
          <Tooltip title="Eraser">
            <Delete />
          </Tooltip>
        </ToggleButton>
      </ToggleButtonGroup>

      <Box sx={{ ml: 2, display: 'flex', gap: 1 }}>
        <Button
          variant="contained"
          size="small"
          startIcon={<Save />}
          onClick={onSave}
        >
          Save
        </Button>
        <Button
          variant="outlined"
          size="small"
          startIcon={<Download />}
          onClick={(e) => setExportMenuAnchor(e.currentTarget)}
        >
          Export
        </Button>
      </Box>

      <Menu
        anchorEl={exportMenuAnchor}
        open={Boolean(exportMenuAnchor)}
        onClose={() => setExportMenuAnchor(null)}
      >
        <MenuItem onClick={() => { onExport('coco'); setExportMenuAnchor(null) }}>
          COCO JSON
        </MenuItem>
        <MenuItem onClick={() => { onExport('geojson'); setExportMenuAnchor(null) }}>
          GeoJSON
        </MenuItem>
        <MenuItem onClick={() => { onExport('csv'); setExportMenuAnchor(null) }}>
          CSV
        </MenuItem>
      </Menu>
    </Box>
  )
}
