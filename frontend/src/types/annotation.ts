export interface Annotation {
  id: number
  wsi_file_id: number
  geometry: {
    type: string
    coordinates: any
  }
  geometry_type: string
  label: string
  label_hierarchy?: string[]
  color?: string
  opacity: number
  description?: string
  confidence?: number
  is_ai_generated: boolean
  ai_model_version?: string
  layer_name: string
  is_locked: boolean
  is_visible: boolean
  area_um2?: number
  perimeter_um?: number
  centroid_x?: number
  centroid_y?: number
  version: number
  parent_annotation_id?: number
  creator_id: number
  created_at: string
  updated_at: string
}

export interface LabelClass {
  name: string
  color: string
  description?: string
  children?: LabelClass[]
}

export interface LabelSchema {
  id: number
  name: string
  description?: string
  version: string
  schema_definition: {
    classes: LabelClass[]
  }
  is_default: boolean
  is_active: boolean
}
