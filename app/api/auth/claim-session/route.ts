import { randomUUID } from "crypto"
import { NextResponse } from "next/server"

import { supabaseAdmin } from "@/src/lib/supabase-admin"

export const runtime = "nodejs"

function readBearerToken(request: Request) {
  const authorization = request.headers.get("authorization") ?? ""
  const match = authorization.match(/^Bearer\s+(.+)$/i)

  return match?.[1] ?? null
}

export async function POST(request: Request) {
  const accessToken = readBearerToken(request)

  if (!accessToken) {
    return NextResponse.json({ error: "Not authenticated." }, { status: 401 })
  }

  const {
    data: { user },
    error: userError,
  } = await supabaseAdmin.auth.getUser(accessToken)

  if (userError || !user) {
    return NextResponse.json(
      { error: "Your session has expired. Please log in again." },
      { status: 401 }
    )
  }

  const sessionToken = randomUUID()

  const { error } = await supabaseAdmin
    .from("Profiles")
    .update({ active_session_id: sessionToken })
    .eq("id", user.id)

  if (error) {
    return NextResponse.json(
      { error: "Could not start your session." },
      { status: 500 }
    )
  }

  return NextResponse.json({ sessionToken })
}
