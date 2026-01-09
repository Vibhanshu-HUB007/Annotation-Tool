import { useEffect, useRef } from 'react'
import OpenSeadragon from 'openseadragon'
import { fabric } from 'fabric'
import { Annotation } from '../types/annotation'

interface AnnotationOverlayProps {
  viewer: OpenSeadragon.Viewer
  wsiId: number
  annotations: Annotation[]
}

export function AnnotationOverlay({
  viewer,
  annotations,
}: AnnotationOverlayProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const fabricCanvasRef = useRef<fabric.Canvas | null>(null)

  useEffect(() => {
    if (!viewer) return

    const viewport = viewer.viewport
    const container = viewer.container

    // Create canvas for annotations
    const canvas = document.createElement('canvas')
    canvas.style.position = 'absolute'
    canvas.style.top = '0'
    canvas.style.left = '0'
    canvas.style.pointerEvents = 'none'
    container.appendChild(canvas)
    canvasRef.current = canvas

    // Initialize Fabric.js canvas
    const fabricCanvas = new fabric.Canvas(canvas, {
      width: container.clientWidth,
      height: container.clientHeight,
      selection: false,
    })
    fabricCanvasRef.current = fabricCanvas

    // Update canvas size on resize
    const updateCanvasSize = () => {
      const bounds = container.getBoundingClientRect()
      canvas.width = bounds.width
      canvas.height = bounds.height
      fabricCanvas.setDimensions({
        width: bounds.width,
        height: bounds.height,
      })
      fabricCanvas.renderAll()
    }

    updateCanvasSize()
    window.addEventListener('resize', updateCanvasSize)

    // Update canvas on viewport change
    const updateAnnotations = () => {
      if (!fabricCanvas) return
      fabricCanvas.clear()

      const zoom = viewport.getZoom()

      annotations.forEach((ann) => {
        if (!ann.is_visible) return

        const geometry = ann.geometry
        if (geometry.type === 'Polygon') {
          const points = geometry.coordinates[0].map((coord: number[]) => {
            const point = viewport.pixelFromPoint(
              new OpenSeadragon.Point(coord[0], coord[1])
            )
            return {
              x: point.x * zoom,
              y: point.y * zoom,
            }
          })

          const polygon = new fabric.Polygon(points, {
            fill: ann.color || '#FF0000',
            opacity: ann.opacity || 0.7,
            stroke: ann.color || '#FF0000',
            strokeWidth: 2,
            selectable: false,
            evented: false,
          })

          fabricCanvas.add(polygon)
        }
      })

      fabricCanvas.renderAll()
    }

    viewer.addHandler('viewport-change', updateAnnotations)
    updateAnnotations()

    return () => {
      window.removeEventListener('resize', updateCanvasSize)
      viewer.removeHandler('viewport-change', updateAnnotations)
      if (fabricCanvas) {
        fabricCanvas.dispose()
      }
      if (canvas && canvas.parentNode) {
        canvas.parentNode.removeChild(canvas)
      }
    }
  }, [viewer, annotations])

  return null
}
