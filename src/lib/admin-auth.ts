import "server-only"

import type { User } from "@supabase/supabase-js"
import { NextResponse } from "next/server"

import { supabaseAdmin } from "@/src/lib/supabase-admin"

function readBearerToken(request: Request) {
  const authorization = request.headers.get("authorization") ?? ""
  const match = authorization.match(/^Bearer\s+(.+)$/i)

  return match?.[1] ?? null
}

/**
 * Resolves the caller from their Supabase access token and confirms they are
 * listed in the Admins table. Returns the user, or a ready-made error
 * response to send back unchanged.
 */
export async function requireAdmin(
  request: Request
): Promise<{ user: User } | { response: NextResponse }> {
  const accessToken = readBearerToken(request)

  if (!accessToken) {
    return {
      response: NextResponse.json({ error: "Not authenticated." }, { status: 401 }),
    }
  }

  const {
    data: { user },
    error: userError,
  } = await supabaseAdmin.auth.getUser(accessToken)

  if (userError || !user) {
    return {
      response: NextResponse.json(
        { error: "Your session has expired. Please log in again." },
        { status: 401 }
      ),
    }
  }

  const { data: adminRow, error: adminError } = await supabaseAdmin
    .from("Admins")
    .select("user_id")
    .eq("user_id", user.id)
    .maybeSingle()

  if (adminError) {
    return {
      response: NextResponse.json(
        { error: "Could not check admin access." },
        { status: 500 }
      ),
    }
  }

  if (!adminRow) {
    return {
      response: NextResponse.json({ error: "Admins only." }, { status: 403 }),
    }
  }

  return { user }
}
