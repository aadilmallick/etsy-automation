import express, { application, Request, Response } from "express";
import axios, { AxiosError } from "axios";
import config, { getOAuthURL } from "./config";
import cors from "cors";
import path from "path";
const app = express();
app.use(express.static("dist"));
app.use(
  cors({
    origin: "*",
    methods: ["GET", "POST", "DELETE", "PUT", "PATCH"],
  })
);
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
const port = config.port;
app.get("/", (req: Request, res: Response) => {
  res.sendFile(__dirname + "dist/index.html");
});

app.get("/api/request-oauth-code", async (req: Request, res: Response) => {
  const { url, clientVerifier } = getOAuthURL();
  app.locals.clientVerifier = clientVerifier;
  return res.json({ url });
});

app.post("/api/create-listings", async (req: Request, res: Response) => {});

app.get("/api/ping", async (req: Request, res: Response) => {
  try {
    const response = await axios.get(
      "https://api.etsy.com/v3/application/openapi-ping",
      {
        headers: {
          "x-api-key": config.KEY_SECRET,
          "Content-Type": "application/json",
        },
      }
    );

    res.json(response.data);
  } catch (e) {
    if (e instanceof AxiosError) {
    }
    console.log(e);
    res.status(500).json({
      message: "An error occurred while trying to ping Etsy's API.",
    });
  }
});

app.get("/api/oauth/redirect", async (req: Request, res: Response) => {
  // The req.query object has the query params that Etsy authentication sends
  // to this route. The authorization code is in the `code` param
  const authCode = req.query.code;
  if (!authCode) {
    console.log(req.query);
    res.status(400).send("No auth code provided");
  }
  if (!app.locals.clientVerifier) {
    res.status(400).send("No client verifier found");
  }
  const tokenUrl = "https://api.etsy.com/v3/public/oauth/token";
  const redirect_uri =
    process.env.NODE_ENV === "production"
      ? `${config.VITE_API_URL_PRODUCTION}/api/oauth/redirect`
      : `http://localhost:${port}/api/oauth/redirect`;
  const requestOptions = {
    method: "POST",
    body: JSON.stringify({
      grant_type: "authorization_code",
      client_id: config.KEY_SECRET,
      redirect_uri: redirect_uri,
      code: authCode,
      code_verifier: app.locals.clientVerifier,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  };

  const response = await fetch(tokenUrl, requestOptions);

  // Extract the access token from the response access_token data field
  if (response.ok) {
    const tokenData = (await response.json()) as { access_token: string };
    console.log("Token data");
    console.log(tokenData);
    app.locals.tokenData = tokenData;
    res.redirect(`/welcome?access_token=${tokenData.access_token}`);
    // res.json(tokenData);
  } else {
    res.send("oops");
  }
});

app.get("/api/accesstoken", async (req: Request, res: Response) => {
  return res.json({
    access_token: app.locals.access_token || null,
    token_data: app.locals.tokenData || null,
  });
});

// gets new access token
app.get("/api/refreshtoken", async (req: Request, res: Response) => {
  if (!app.locals.tokenData) {
    return res.status(400).json({ error: "No token data found" });
  }
  const url = `https://api.etsy.com/v3/public/oauth/token?grant_type=refresh_token&client_id=${config.KEY_SECRET}&refresh_token=${app.locals.tokenData.refresh_token}`;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
  if (response.ok) {
    const tokenData = (await response.json()) as {
      access_token: string;
      refresh_token: string;
    };
    app.locals.tokenData = tokenData;
    return res.json(tokenData);
  } else {
    return res.status(500).json({
      error: "Failed to refresh token",
    });
  }
});

app.get("/welcome", async (req: Request, res: Response) => {
  const { access_token } = req.query;
  if (!access_token) {
    res.status(400).send("No access token found");
  }
  app.locals.access_token = access_token;
  return res.sendFile(path.join(__dirname, "welcome.html"));

  // const requestOptions = {
  //   headers: {
  //     "x-api-key": config.KEY_SECRET,
  //     // Scoped endpoints require a bearer token
  //     Authorization: `Bearer ${access_token}`,
  //   },
  // };

  // const response = await fetch(
  //   `https://api.etsy.com/v3/application/users/${user_id}`,
  //   requestOptions
  // );
});

app.listen(port, () => {
  console.log("Current environment: ", process.env.NODE_ENV);
  console.log(`Server is running on http://localhost:${port}`);
});
