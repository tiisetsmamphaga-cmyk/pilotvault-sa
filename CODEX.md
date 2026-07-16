# PilotVault SA

## Project Overview

PilotVault SA is a premium South African aviation exam preparation platform built specifically for SACAA student pilots.

Mission:

Help South African student pilots pass their SACAA exams with confidence through realistic question banks, mock exams, analytics, and detailed explanations.

Brand personality:

- Premium
- Professional
- Aviation focused
- Modern SaaS
- Built by pilots for pilots

---

# Tech Stack

Frontend

- Next.js (App Router)
- React
- TypeScript
- Tailwind CSS
- Framer Motion
- Lucide React

Backend

- Supabase

Deployment

- GitHub
- Vercel

---

# Brand Colors

Background

#06111f

Cards

#081726

Borders

#1e3a5f

Accent

#f4b400

Text

White

---

# UI Guidelines

Always maintain the existing PilotVault design.

Requirements:

- Premium appearance
- Dark navy background
- Gold accents
- Rounded cards
- Soft shadows
- Smooth Framer Motion animations
- Mobile-first
- Consistent spacing
- Large readable typography

Never introduce bright colors that don't match the brand.

Avoid generic loading spinners.

---

# Design Principles

Every page should feel like modern aviation software.

Think Garmin.

Think ForeFlight.

Think airline operations software.

Not a generic dashboard.

---

# Coding Standards

Always:

- Create reusable components
- Keep components small
- Prefer composition over duplication
- Use TypeScript types
- Keep Tailwind classes clean
- Preserve existing functionality
- Avoid breaking Supabase queries

Never remove existing business logic unless requested.

---

# Current Product

Completed

- Landing page
- Authentication
- Dashboard
- Subject access
- Trial accounts
- PPL subscriptions
- Individual subject purchases
- Practice mode
- Mock exams
- Topic practice
- Question explanations
- Results page

Current work

Building the SACAA PPL question database.

---

# Database

Questions table contains

- subject
- topic
- question
- option_a
- option_b
- option_c
- option_d
- correct_answer
- explanation
- image_url
- is_trial_question

Do not modify schema unless requested.

---

# Important Rules

Never change:

- Authentication flow
- Subscription logic
- Subject access logic
- Trial logic
- Database structure

unless explicitly requested.

---

# Preferred Development Style

When implementing features:

1. Create reusable components.

2. Keep files small.

3. Keep UI consistent.

4. Maintain premium animations.

5. Preserve responsiveness.

6. Never rewrite large files unless necessary.

7. Explain major architectural decisions.

---

# Future Roadmap

Upcoming features

- Analytics
- Weak topic tracking
- Admin dashboard
- Payments
- Coupon codes
- Study streaks
- Image support for questions
- Loading animations
- Performance improvements

Always implement with future scalability in mind.

---

# Goal

PilotVault should become the leading SACAA exam preparation platform in South Africa.

Every design and engineering decision should support this goal.

<!-- Deployment trigger: 2026-07-17 -->
