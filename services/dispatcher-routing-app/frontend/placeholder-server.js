const http = require("http");

const port = process.env.DISPATCHER_FRONTEND_PORT || 4173;

const server = http.createServer((_, res) => {
  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end("dispatcher-frontend placeholder. Replace DISPATCHER_FRONTEND_CMD to run the real app.");
});

server.listen(port, "0.0.0.0", () => {
  // eslint-disable-next-line no-console
  console.log(`Placeholder frontend listening on ${port}`);
});
