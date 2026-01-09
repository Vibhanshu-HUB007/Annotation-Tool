import { create } from 'zustand'
import { Annotation } from '../types/annotation'

interface Viewport {
  bounds: any
  zoom: number
  center: any
}

interface AnnotationState {
  annotations: Annotation[]
  selectedAnnotation: Annotation | null
  currentTool: 'select' | 'freehand' | 'polygon' | 'rectangle' | 'point' | 'erase'
  currentLabel: string
  currentColor: string
  viewport: Viewport | null
  setAnnotations: (annotations: Annotation[]) => void
  addAnnotation: (annotation: Annotation) => void
  updateAnnotation: (id: number, updates: Partial<Annotation>) => void
  deleteAnnotation: (id: number) => void
  setSelectedAnnotation: (annotation: Annotation | null) => void
  setCurrentTool: (tool: AnnotationState['currentTool']) => void
  setCurrentLabel: (label: string) => void
  setCurrentColor: (color: string) => void
  setViewport: (viewport: Viewport) => void
}

export const useAnnotationStore = create<AnnotationState>((set) => ({
  annotations: [],
  selectedAnnotation: null,
  currentTool: 'select',
  currentLabel: 'Dysplastic Epithelial Cells',
  currentColor: '#FF8800',
  viewport: null,
  setAnnotations: (annotations) => set({ annotations }),
  addAnnotation: (annotation) =>
    set((state) => ({ annotations: [...state.annotations, annotation] })),
  updateAnnotation: (id, updates) =>
    set((state) => ({
      annotations: state.annotations.map((ann) =>
        ann.id === id ? { ...ann, ...updates } : ann
      ),
    })),
  deleteAnnotation: (id) =>
    set((state) => ({
      annotations: state.annotations.filter((ann) => ann.id !== id),
    })),
  setSelectedAnnotation: (annotation) => set({ selectedAnnotation: annotation }),
  setCurrentTool: (tool) => set({ currentTool: tool }),
  setCurrentLabel: (label) => set({ currentLabel: label }),
  setCurrentColor: (color) => set({ currentColor: color }),
  setViewport: (viewport) => set({ viewport }),
}))
