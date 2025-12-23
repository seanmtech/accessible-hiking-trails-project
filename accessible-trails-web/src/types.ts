export interface AccessibilityPlace {
  name: string;
  url: string;
}

export interface AccessibilityDetails {
  trails: AccessibilityPlace[];
  parking: AccessibilityPlace[];
  camping: AccessibilityPlace[];
  lodging: AccessibilityPlace[];
  restrooms: AccessibilityPlace[];
  general: AccessibilityPlace[];
}

export interface Park {
  id: string;
  name: string;
  state: string;
  lat: number;
  lon: number;
  accessible_restrooms: boolean | null;
  accessible_parking: boolean | null;
  accessible_trails: boolean | null;
  source: 'nps' | 'manual' | 'osm';
  affiliate_links: {
    gear: string | null;
    lodging: string | null;
  };
  status: 'verified' | 'needs_review';
  reviewer_notes?: string;
  accessibility_details?: AccessibilityDetails;
}
