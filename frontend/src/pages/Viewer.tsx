import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Box, Drawer, Typography, IconButton } from '@mui/material'
import { Close } from '@mui/icons-material'
import { useState, useEffect } from 'react'
import api from '../api/client'
import { WSIViewer } from '../components/WSIViewer'
import { AnnotationToolbar } from '../components/AnnotationToolbar'
import { AnnotationPanel } from '../components/AnnotationPanel'
import { useAnnotationStore } from '../store/annotationStore'
import toast from 'react-hot-toast'

interface WSIFile {
  id: number
  filename: string
  original_filename: string
  width: number
  height: number
  file_path: string
}

export default function Viewer() {
  const { wsiId } = useParams<{ wsiId: string }>()
  const [panelOpen, setPanelOpen] = useState(true)
  const { setAnnotations } = useAnnotationStore()

  const { data: wsiFile, isLoading } = useQuery<WSIFile>({
    queryKey: ['wsi-file', wsiId],
    queryFn: async () => {
      const response = await api.get(`/wsi/${wsiId}`)
      return response.data
    },
    enabled: !!wsiId,
  })

  const { data: wsiAnnotations } = useQuery<unknown[]>({
    queryKey: ['annotations', wsiId],
    queryFn: async () => {
      const response = await api.get(`/annotations/wsi/${wsiId}`)
      return response.data
    },
    enabled: !!wsiId,
  })

  useEffect(() => {
    if (wsiAnnotations) {
      setAnnotations(wsiAnnotations as any)
    }
  }, [wsiAnnotations, setAnnotations])

  const handleSave = async () => {
    try {
      // Save annotations logic
      toast.success('Annotations saved')
    } catch (error) {
      toast.error('Failed to save annotations')
    }
  }

  const handleExport = async (format: 'coco' | 'geojson' | 'csv') => {
    try {
      const response = await api.get(`/export/wsi/${wsiId}/${format}`, {
        responseType: 'blob',
      })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${wsiFile?.original_filename}_annotations.${format}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      toast.success(`Exported as ${format.toUpperCase()}`)
    } catch (error) {
      toast.error('Export failed')
    }
  }

  if (isLoading || !wsiFile) {
    return <Box>Loading...</Box>
  }

  // For now, use a placeholder tile source
  // In production, this would be a DeepZoom or IIIF tile source
  const tileSource = `/api/wsi/${wsiId}/tile?level=0&x=0&y=0&format=jpeg`

  return (
    <Box sx={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
      <Box sx={{ flex: 1, position: 'relative' }}>
        <AnnotationToolbar onSave={handleSave} onExport={handleExport} />
        <WSIViewer
          wsiId={parseInt(wsiId!)}
          width={wsiFile.width}
          height={wsiFile.height}
          tileSource={tileSource}
        />
      </Box>

      <Drawer
        anchor="right"
        open={panelOpen}
        onClose={() => setPanelOpen(false)}
        PaperProps={{
          sx: { width: 350 },
        }}
      >
        <Box sx={{ p: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6">Annotations</Typography>
            <IconButton size="small" onClick={() => setPanelOpen(false)}>
              <Close />
            </IconButton>
          </Box>
          <AnnotationPanel wsiId={parseInt(wsiId!)} />
        </Box>
      </Drawer>
    </Box>
  )
}
