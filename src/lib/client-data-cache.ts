import type { User } from "@supabase/supabase-js"

import { supabase } from "@/src/lib/supabase"

const CLIENT_CACHE_TTL_MS = 5 * 60 * 1000

export type CachedLicenceLevel = "ppl" | "cpl" | "atpl"

export type CachedProfile = {
  full_name: string
  email: string | null
  licence_level: CachedLicenceLevel | null
  subscription_status: string | null
  subscription_plan: string | null
  payment_status: string | null
  trial_ends_at: string | null
  subscription_expires_at: string | null
}

export type CachedSubjectAccess = {
  subject: string
  access_status: string | null
  expires_at: string
}

let userRequest: Promise<User | null> | null = null

let profileUserId: string | null = null
let profileRequest: Promise<CachedProfile> | null = null
let profileCachedAt = 0

let accessUserId: string | null = null
let accessRequest: Promise<CachedSubjectAccess[]> | null = null
let accessCachedAt = 0

let authListenerStarted = false

function cacheIsFresh(cachedAt: number) {
  return Date.now() - cachedAt < CLIENT_CACHE_TTL_MS
}

function resetProfileCache() {
  profileUserId = null
  profileRequest = null
  profileCachedAt = 0
}

function resetAccessCache() {
  accessUserId = null
  accessRequest = null
  accessCachedAt = 0
}

function ensureAuthListener() {
  if (authListenerStarted || typeof window === "undefined") return

  authListenerStarted = true

  supabase.auth.onAuthStateChange((event, session) => {
    if (event === "SIGNED_OUT") {
      clearClientDataCache()
      return
    }

    if (session?.user) {
      userRequest = Promise.resolve(session.user)
    }

    if (event === "USER_UPDATED") {
      resetProfileCache()
    }
  })
}

export function clearClientDataCache() {
  userRequest = null
  resetProfileCache()
  resetAccessCache()
}

export async function getCachedCurrentUser(options?: {
  force?: boolean
}): Promise<User | null> {
  ensureAuthListener()

  if (!userRequest || options?.force) {
    userRequest = supabase.auth
      .getUser()
      .then(({ data, error }) => {
        if (error) throw error
        return data.user
      })
      .catch((error) => {
        userRequest = null
        throw error
      })
  }

  return userRequest
}

export async function getCachedProfile(
  userId: string,
  options?: { force?: boolean }
): Promise<CachedProfile> {
  const shouldRefresh =
    options?.force ||
    profileUserId !== userId ||
    !profileRequest ||
    !cacheIsFresh(profileCachedAt)

  if (shouldRefresh) {
    profileUserId = userId
    profileCachedAt = Date.now()

    profileRequest = supabase
      .from("Profiles")
      .select(
        "full_name, email, licence_level, subscription_status, subscription_plan, payment_status, trial_ends_at, subscription_expires_at"
      )
      .eq("id", userId)
      .single()
      .then(({ data, error }) => {
        if (error) throw error
        return data as CachedProfile
      })
      .catch((error) => {
        resetProfileCache()
        throw error
      })
  }

  return profileRequest!
}

export async function getCachedSubjectAccess(
  userId: string,
  options?: { force?: boolean }
): Promise<CachedSubjectAccess[]> {
  const shouldRefresh =
    options?.force ||
    accessUserId !== userId ||
    !accessRequest ||
    !cacheIsFresh(accessCachedAt)

  if (shouldRefresh) {
    accessUserId = userId
    accessCachedAt = Date.now()

    accessRequest = supabase
      .from("SubjectAccess")
      .select("subject, access_status, expires_at")
      .eq("user_id", userId)
      .then(({ data, error }) => {
        if (error) throw error
        return (data ?? []) as CachedSubjectAccess[]
      })
      .catch((error) => {
        resetAccessCache()
        throw error
      })
  }

  return accessRequest!
}

export function updateCachedProfile(patch: Partial<CachedProfile>) {
  if (!profileRequest) return

  profileRequest = profileRequest.then((profile) => ({
    ...profile,
    ...patch,
  }))
  profileCachedAt = Date.now()
}
