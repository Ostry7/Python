import express from "express";
import mysql from "mysql2/promise";

const app = express();

const dbConfig = {
  host: process.env.DB_HOST || "mysql-service",
  user: process.env.DB_USER || "root",
  password: process.env.DB_PASSWORD,
  database: process.env.DB_DATABASE || "maindb",
  port: process.env.DB_PORT || 3306,
};

app.get("/health", async (req, res) => {
  try {
    const connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.query("SELECT NOW() AS now");
    await connection.end();

    res.json({
      status: "ok",
      mysql_time: rows[0].now,
    });
  } catch (err) {
    res.status(500).json({
      status: "error",
      error: err.message,
    });
  }
});

// ✅ Klucz: nasłuch na 0.0.0.0, aby był dostępny z zewnątrz Poda
app.listen(3000, "0.0.0.0", () => console.log("Backend działa na porcie 3000"));
