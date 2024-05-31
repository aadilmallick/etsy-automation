import crypto from "crypto";

type ClassKeys = keyof Config;

class Config {
  public readonly KEY_SECRET: string;
  public readonly SHARED_SECRET: string;
  public readonly port = process.env.NODE_ENV === "production" ? 80 : 3003;
  constructor() {
    this.KEY_SECRET = process.env.KEY_SECRET || "";
    this.SHARED_SECRET = process.env.SHARED_SECRET || "";
    this.validateKey("KEY_SECRET");
    this.validateKey("SHARED_SECRET");
  }

  private validateKey(key: ClassKeys) {
    if (!this[key]) {
      throw new Error(`${key} is not defined`);
    }
  }
}

const config = new Config();
export default config;

export function getOAuthURL() {
  const base64URLEncode = (str: any): string =>
    str
      .toString("base64")
      .replace(/\+/g, "-")
      .replace(/\//g, "_")
      .replace(/=/g, "");

  const sha256 = (buffer: string) =>
    crypto.createHash("sha256").update(buffer).digest();

  // We’ll use the verifier to generate the challenge.
  // The verifier needs to be saved for a future step in the OAuth flow.
  const codeVerifier = base64URLEncode(crypto.randomBytes(32));

  // With these functions, we can generate
  // the values needed for our OAuth authorization grant.
  const codeChallenge = base64URLEncode(sha256(codeVerifier));
  const state = Math.random().toString(36).substring(7);
  const scopes = "listings_w%20shops_w%20shops_r%20listings_r";
  return {
    url: `https://www.etsy.com/oauth/connect?response_type=code&redirect_uri=http://localhost:${config.port}/oauth/redirect&scope=listings_w%20shops_w&client_id=${config.KEY_SECRET}&state=${state}&code_challenge=${codeChallenge}&code_challenge_method=S256`,
    clientVerifier: codeVerifier,
    codeChallenge,
    state,
  };
}
