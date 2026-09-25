import type { LucideIcon } from "lucide-react"
import {
  Brain,
  Cloud,
  Compass,
  Map,
  Plane,
  Radio,
  Scale,
  Wrench,
} from "lucide-react"

export type PplSubject = {
  slug: string
  name: string
  icon: LucideIcon
  // One line for the subject cards on /subjects.
  summary: string
  // Opening paragraph of the subject's own page.
  intro: string
  // Short phrase used in the page's search description.
  searchFocus: string
  // Topics as they are tagged in the question bank.
  topics: string[]
}

// Slugs match the subject values used by the practice pages and question bank.
export const PPL_SUBJECTS: PplSubject[] = [
  {
    slug: "air-law",
    name: "Air Law",
    icon: Scale,
    summary:
      "Rules, regulations, airspace classifications, licensing requirements, and operational procedures.",
    intro:
      "The SACAA PPL Air Law exam tests the South African Civil Aviation Regulations that apply to private pilots: licensing and ratings, the rules of the air, airspace and VFR minima, signals and interception, and what to do after an accident or incident. Our Air Law question bank is organised by these topics, so you can practise the rules you will actually be examined on.",
    searchFocus: "licensing, rules of the air, airspace, VFR minima and accident reporting",
    topics: [
      "Accidents, Incidents & SAR",
      "PPL Licensing & Ratings",
      "Rules of the Air",
      "Signals & Interception",
      "Flight Planning & Fuel",
      "Definitions & Documents",
      "Logbooks & Flight Records",
      "Aircraft Equipment & Operations",
      "VFR & Weather Minima",
      "Medical, Fitness & Recency",
      "Aerodromes & Ground Operations",
      "Airspace & Altimetry",
      "Passengers & Safety",
    ],
  },
  {
    slug: "meteorology",
    name: "Meteorology",
    icon: Cloud,
    summary:
      "Weather systems, forecasts, METARs, TAFs, clouds, wind, and aviation weather interpretation.",
    intro:
      "Meteorology covers how the atmosphere behaves and how weather affects your flight: pressure, temperature and humidity, wind, clouds and precipitation, air masses and fronts, stability, and reading aviation weather reports. It includes South African weather patterns, so you prepare for the conditions you will actually fly in.",
    searchFocus: "clouds, pressure, wind, fronts, weather reports and South African weather",
    topics: [
      "Clouds & Precipitation",
      "Meteorological Reports",
      "Pressure",
      "Wind",
      "South African Weather",
      "Temperature",
      "Humidity",
      "Fronts",
      "Atmosphere",
      "Stability & Lapse Rates",
      "Air Masses",
      "Air Density",
    ],
  },
  {
    slug: "navigation",
    name: "Navigation",
    icon: Compass,
    summary:
      "Maps, charts, headings, tracks, magnetic variation, flight calculations, and navigation principles.",
    intro:
      "Navigation tests the technique and calculations of getting from A to B: the earth and coordinates, chart projections and scale, magnetism and the compass, the wind triangle and flight computer, groundspeed and fuel, radio navigation and position fixing, and diversions. Practise the calculations until they become routine.",
    searchFocus: "charts, the compass, the wind triangle, flight computer calculations and radio navigation",
    topics: [
      "Flight Planning, Groundspeed & Fuel",
      "Magnetism & Compass",
      "Wind Triangle & Flight Computer",
      "Chart Projections & Scale",
      "Radio Navigation & Position Fixing",
      "Earth, Coordinates & Time",
      "Airspeed, Altimetry & Density Altitude",
      "Day, Night & Time",
      "Track Error & Diversions",
      "Chart Symbols & Aeronautical Charts",
      "Unit Conversions",
    ],
  },
  {
    slug: "human-performance",
    name: "Human Performance",
    icon: Brain,
    summary:
      "Aviation physiology, fatigue, hypoxia, vision, decision-making, and human factors.",
    intro:
      "Human Performance and Limitations covers how flying affects your body and mind: the atmosphere and hypoxia, vision and visual illusions, hearing and spatial disorientation, stress and fatigue, information processing and decision-making, and fitness to fly.",
    searchFocus: "hypoxia, vision and illusions, disorientation, fatigue and decision-making",
    topics: [
      "Information Processing & Behaviour",
      "Vision & Visual Illusions",
      "Atmosphere, Respiration & Hypoxia",
      "Hearing, Balance & Spatial Orientation",
      "Airmanship & Cockpit Safety",
      "Stress, Fatigue & Sleep",
      "Blood & Circulation",
      "Fitness & Medical Considerations",
      "Pressure Effects & Decompression",
      "Motion Sickness",
      "Acceleration & G-Forces",
      "Carbon Monoxide & Toxic Hazards",
      "Circadian Rhythm & Jet Lag",
    ],
  },
  {
    slug: "principles-of-flight",
    name: "Principles of Flight",
    icon: Plane,
    summary:
      "Aerodynamics, lift, drag, stability, stalls, controls, and aircraft performance.",
    intro:
      "Principles of Flight explains why an aircraft flies and how it behaves: aerofoils and lift, drag, the four forces, stability, flight controls and trim, turns and load factor, stalls and spins, and flap, glide and climb performance.",
    searchFocus: "lift, drag, stability, stalls, turns and load factor",
    topics: [
      "Stability",
      "Aerofoils & Lift",
      "Flaps & Glide",
      "Drag",
      "Turns & Load Factor",
      "Basic Aerodynamics",
      "Trim & Balance Tabs",
      "Stalls",
      "Flight Controls & Axes",
      "ISA & Air Density",
      "Climb Performance",
      "Spins",
      "Aileron Drag",
      "Airspeed Limitations",
      "Four Forces",
      "Wing Design",
      "Airspeed",
    ],
  },
  {
    slug: "aircraft-technical-and-general",
    name: "Aircraft Technical & General",
    icon: Wrench,
    summary:
      "Aircraft systems, engines, instruments, electrics, hydraulics, and maintenance knowledge.",
    intro:
      "Aircraft Technical and General covers how a light aircraft works: piston engines, lubrication and fuel systems, propellers, electrics, hydraulics, airframes and undercarriage, and the pressure, gyroscopic and compass instruments you rely on in the cockpit.",
    searchFocus: "piston engines, flight instruments, electrics, fuel systems and airframes",
    topics: [
      "Piston Engines",
      "Pressure Instruments",
      "Gyroscopic Instruments",
      "Electrics",
      "Airframes",
      "The Magnetic Compass",
      "Undercarriage",
      "Lubrication Systems",
      "Fuel Systems",
      "Propellers",
      "Hydraulic Systems",
    ],
  },
  {
    slug: "radio-telephony",
    name: "Radio Telephony",
    icon: Radio,
    summary:
      "Standard phraseology, radio procedures, emergencies, and communication techniques.",
    intro:
      "Radio Telephony covers how you communicate with air traffic control: standard phraseology and radio procedures, South African airspace, flight plans and flight rules, altimeter setting procedures, the semi-circular rule and runway condition reports.",
    searchFocus: "radio procedures, phraseology, airspace and altimeter setting procedures",
    topics: [
      "Radio Procedures",
      "Airspaces",
      "Flight Planning",
      "Altimeter Setting Procedures",
      "Phraseology",
      "Flight Rules",
      "Semi-Circular Rule",
      "Runway Conditions",
      "Navigation",
    ],
  },
  {
    slug: "flight-planning",
    name: "Flight Planning",
    icon: Map,
    summary:
      "Mass and balance, fuel planning, performance calculations, and flight preparation.",
    intro:
      "Flight Planning and Performance covers preparing a flight safely: mass and balance, take-off, climb, cruise and landing performance, runway distances and slope, fuel planning, range and endurance, V-speeds, and the effects of the atmosphere, wind shear and wake turbulence.",
    searchFocus: "mass and balance, take-off and landing performance and fuel planning",
    topics: [
      "Mass & Balance",
      "Take-off Performance",
      "Cruise, Range & Endurance",
      "Runway Distances & Slope",
      "Fuel Planning",
      "Airspeed & Stall Performance",
      "Wind Shear & Wake Turbulence",
      "Climb Performance",
      "Landing Performance",
      "V-Speeds & Limitations",
      "Atmosphere & Performance",
      "Glide Performance",
      "Runway Surface & Aquaplaning",
    ],
  },
]

export function getPplSubject(slug: string) {
  return PPL_SUBJECTS.find((subject) => subject.slug === slug)
}
