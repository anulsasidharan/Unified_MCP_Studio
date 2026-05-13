/** @type {import('next').NextConfig} */
const backendInternal =
  process.env.BACKEND_INTERNAL_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000";

const nextConfig = {
  reactStrictMode: true,
  /** Same-origin /api/v1 → FastAPI (avoids browser CORS during local dev). */
  async rewrites() {
    return [
      {
        source: "/api/v1/:path*",
        destination: `${backendInternal}/api/v1/:path*`,
      },
    ];
  },
};

export default nextConfig;
