import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

// 1. Define which routes are public (anyone can see them)
// We only want the sign-in and sign-up pages to be public.
const isPublicRoute = createRouteMatcher(['/sign-in(.*)', '/sign-up(.*)'])

export default clerkMiddleware(async (auth, req) => {
  // 2. If the user tries to go to the Chatbot (/) and is NOT logged in...
  if (!isPublicRoute(req)) {
    // ...force them to sign in first.
    await auth.protect()
  }
})

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
  ],
}