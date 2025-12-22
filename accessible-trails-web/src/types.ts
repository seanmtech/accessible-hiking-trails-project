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
  accessible_restrooms: boolean;
  accessible_parking: boolean;
  accessible_trails: boolean;
  source: 'nps' | 'manual' | 'osm';
  affiliate_links: {
    gear: string | null;
    lodging: string | null;
  };
  status: 'verified' | 'needs_review';
  accessibility_details?: AccessibilityDetails;
}
