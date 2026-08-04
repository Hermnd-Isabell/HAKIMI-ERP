// Project color palette - single source of truth for UI styling.
// Never hard-code these values directly in components.

export const COLORS = {
  // Primary brand
  primary: '#436850',
  primaryDark: '#2d4a38',
  primaryLight: '#365440',

  // Background
  background: '#FBFADA',
  backgroundGradientStart: '#FBFADA',
  backgroundGradientEnd: '#f5f3d8',
  cardGradientStart: '#fdfce8',
  cardGradientEnd: '#f7f5d1',

  // Text
  text: '#12372A',
  textMuted: 'rgba(18, 55, 42, 0.7)',
  textLight: 'rgba(18, 55, 42, 0.5)',
  textExtraLight: 'rgba(18, 55, 42, 0.45)',
  textDisabled: 'rgba(18, 55, 42, 0.35)',
  textPlaceholder: 'rgba(18, 55, 42, 0.25)',

  // Accent / border
  accent: '#ADBC9F',
  accentTransparent: 'rgba(173, 188, 159, 0.45)',
  accentHover: 'rgba(173, 188, 159, 0.7)',
  border: 'rgba(173, 188, 159, 0.4)',
  borderLight: 'rgba(173, 188, 159, 0.18)',

  // Semantic
  danger: '#D9534F',
  dangerLight: 'rgba(217, 83, 79, 0.08)',
  warning: '#F0AD4E',
  warningLight: 'rgba(240, 173, 78, 0.12)',
  success: '#436850',
  successLight: 'rgba(67, 104, 80, 0.1)',

  // Sidebar
  sidebarBg: 'rgba(18, 55, 42, 0.92)',
  sidebarText: '#FBFADA',
  sidebarTextMuted: 'rgba(251, 250, 218, 0.6)',

  // Light surfaces
  white: '#ffffff',
  cream: '#FBFADA',
} as const

export type ColorKey = keyof typeof COLORS
