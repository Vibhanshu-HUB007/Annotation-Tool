import { useEffect, useRef, useState } from 'react'
import OpenSeadragon from 'openseadragon'
import { Box } from '@mui/material'
import { AnnotationOverlay } from './AnnotationOverlay'
import { useAnnotationStore } from '../store/annotationStore'

interface WSIViewerProps {
  wsiId: number
  width: number
  height: number
  tileSource: string
}

export function WSIViewer({ wsiId, width, height, tileSource }: WSIViewerProps) {
  const viewerRef = useRef<HTMLDivElement>(null)
  const [viewer, setViewer] = useState<OpenSeadragon.Viewer | null>(null)
  const { annotations, setViewport } = useAnnotationStore()

  useEffect(() => {
    if (!viewerRef.current) return

    // Custom tile source for WSI
    const customTileSource = {
      getTileUrl: (level: number, x: number, y: number) => {
        return `${tileSource}?level=${level}&x=${x * 256}&y=${y * 256}&format=jpeg`
      },
      width: width,
      height: height,
      tileSize: 256,
      tileOverlap: 0,
      minLevel: 0,
      maxLevel: 10,
      getLevelScale: (level: number) => {
        return 1 / Math.pow(2, level)
      },
      getNumTiles: (level: number) => {
        const scale = 1 / Math.pow(2, level)
        const levelWidth = Math.ceil(width * scale)
        const levelHeight = Math.ceil(height * scale)
        return {
          x: Math.ceil(levelWidth / 256),
          y: Math.ceil(levelHeight / 256),
        }
      },
    }

    const osdViewer = OpenSeadragon({
      element: viewerRef.current,
      prefixUrl: 'https://openseadragon.github.io/openseadragon/images/',
      tileSources: customTileSource,
      showNavigationControl: true,
      showRotationControl: true,
      showFullPageControl: true,
      gestureSettingsMouse: {
        clickToZoom: false,
        dblClickToZoom: true,
        pinchToZoom: true,
        flickEnabled: true,
        flickMinSpeed: 20,
        flickMomentum: 0.25,
      },
    })

    osdViewer.addHandler('viewport-change', () => {
      const viewport = osdViewer.viewport
      setViewport({
        bounds: viewport.getBounds(),
        zoom: viewport.getZoom(),
        center: viewport.getCenter(),
      })
    })

    setViewer(osdViewer)

    return () => {
      osdViewer.destroy()
    }
  }, [wsiId, width, height, tileSource, setViewport])

  return (
    <Box sx={{ position: 'relative', width: '100%', height: '100%' }}>
      <div ref={viewerRef} style={{ width: '100%', height: '100%' }} />
      {viewer && (
        <AnnotationOverlay
          viewer={viewer}
          wsiId={wsiId}
          annotations={annotations}
        />
      )}
    </Box>
  )
}
