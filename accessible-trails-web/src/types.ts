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
}
