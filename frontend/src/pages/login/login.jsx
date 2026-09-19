import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import apiClient from "../../api/client";
import styles from "./login.module.css";

const Login = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState({}); // Field-wise custom errors ke liye
  const [success, setSuccess] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    // Jaise hi user type kare, us field ka error hata dein
    setFieldErrors({ ...fieldErrors, [e.target.name]: "" });
    setError("");
  };

  // Login Form Validation Function
  const validateForm = () => {
    let errors = {};
    let isValid = true;

    // 1. Email Validation (Regex)
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!formData.email.trim()) {
      errors.email = "Email address is required.";
      isValid = false;
    } else if (!emailRegex.test(formData.email)) {
      errors.email = "Please enter a valid email address.";
      isValid = false;
    }

    // 2. Password Validation
    if (!formData.password) {
      errors.password = "Password is required.";
      isValid = false;
    }

    setFieldErrors(errors);
    return isValid;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Pehle custom validation run karein
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");

    try {
      await apiClient.post("/login/", {
        email: formData.email,
        password: formData.password,
      });

      setSuccess("Login successful! Redirecting...");

      setTimeout(() => {
        navigate("/dashboard"); // Success ke baad dashboard par redirect
      }, 1500);
    } catch (err) {
      const responseData = err.response?.data;

      if (responseData) {
        if (typeof responseData === "string") {
          setError(responseData);
        } else if (responseData.message) {
          setError(responseData.message);
        } else if (responseData.error) {
          setError(responseData.error);
        } else {
          const firstError = Object.values(responseData)[0];

          if (Array.isArray(firstError)) {
            setError(firstError[0]);
          } else if (typeof firstError === "string") {
            setError(firstError);
          } else {
            setError(
              "Invalid credentials. Please check your email or password.",
            );
          }
        }
      } else {
        setError("Unable to connect to the server.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.loginContainer}>
      <div className={styles.loginCard}>
        {/* Brand Section (Left) */}
        <div className={styles.brandSection}>
          <div className={styles.brandContent}>
            <span className={styles.badge}>TASK MANAGER</span>
            <h1>Welcome Back! Ready to Get Things Done?</h1>
            <p>
              Log in to access your workspace, manage your ongoing tasks, and
              stay on top of your goals.
            </p>
          </div>
          <div className={styles.circleGraphic1}></div>
          <div className={styles.circleGraphic2}></div>
        </div>

        {/* Form Section (Right) */}
        <div className={styles.formSection}>
          <div className={styles.formHeader}>
            <h2>Member Login</h2>
            <p>Please enter your credentials to sign in.</p>
          </div>

          {error && <div className={styles.errorAlert}>{error}</div>}
          {success && <div className={styles.successAlert}>{success}</div>}

          <form onSubmit={handleSubmit} className={styles.form} noValidate>
            {/* Email */}
            <div className={styles.inputGroup}>
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                name="email"
                placeholder="name@example.com"
                value={formData.email}
                onChange={handleChange}
              />
              {fieldErrors.email && (
                <span
                  style={{
                    color: "#ef4444",
                    fontSize: "12px",
                    marginTop: "4px",
                  }}
                >
                  {fieldErrors.email}
                </span>
              )}
            </div>

            {/* Password */}
            <div className={styles.inputGroup}>
              <div className={styles.passwordHeaderLabel}>
                <label htmlFor="password">Password</label>
                <Link to="/forgot-password" className={styles.forgotInline}>
                  Forgot?
                </Link>
              </div>
              <div className={styles.passwordWrapper}>
                <input
                  type={showPassword ? "text" : "password"}
                  id="password"
                  name="password"
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={handleChange}
                />
                <button
                  type="button"
                  className={styles.eyeBtn}
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
              {fieldErrors.password && (
                <span
                  style={{
                    color: "#ef4444",
                    fontSize: "12px",
                    marginTop: "4px",
                  }}
                >
                  {fieldErrors.password}
                </span>
              )}
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              className={styles.submitBtn}
              disabled={loading}
            >
              {loading ? "Logging in..." : "Log In"}
            </button>
          </form>

          {/* Footer & Links */}
          <div className={styles.footerLinks}>
            <p>
              Don't have an account? <Link to="/signup">Sign up</Link>
            </p>

            <div className={styles.subLinks}>
              <Link to="/forgot-password">Reset Password</Link>
              <span>•</span>
              <Link to="/support">Need Help?</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
