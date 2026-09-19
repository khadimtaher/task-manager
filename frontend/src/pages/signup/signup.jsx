import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import apiClient from "../../api/client";
import styles from "./signup.module.css";

const Signup = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    password: "",
    confirm_password: "",
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

  // Custom Validation Function
  const validateForm = () => {
    let errors = {};
    let isValid = true;

    // 1. Full Name Validation
    if (!formData.full_name.trim()) {
      errors.full_name = "Full name is required.";
      isValid = false;
    } else if (formData.full_name.trim().length < 3) {
      errors.full_name = "Full name must be at least 3 characters long.";
      isValid = false;
    }

    // 2. Email Validation (Regex)
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!formData.email.trim()) {
      errors.email = "Email address is required.";
      isValid = false;
    } else if (!emailRegex.test(formData.email)) {
      errors.email = "Please enter a valid email address.";
      isValid = false;
    }

    // 3. Password Custom Rules Validation
    const password = formData.password;
    if (!password) {
      errors.password = "Password is required.";
      isValid = false;
    } else {
      if (password.length < 8) {
        errors.password = "Password must be at least 8 characters long.";
        isValid = false;
      } else if (!/[A-Z]/.test(password)) {
        errors.password = "Password must contain at least one uppercase letter.";
        isValid = false;
      } else if (!/[a-z]/.test(password)) {
        errors.password = "Password must contain at least one lowercase letter.";
        isValid = false;
      } else if (!/[0-9]/.test(password)) {
        errors.password = "Password must contain at least one number.";
        isValid = false;
      }
    }

    // 4. Confirm Password Match Validation
    if (formData.password !== formData.confirm_password) {
      errors.confirm_password = "Passwords do not match!";
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
      await apiClient.post("/signup/", {
        full_name: formData.full_name,
        email: formData.email,
        password: formData.password,
        confirm_password: formData.confirm_password,
      });

      setSuccess("Account created successfully! Redirecting...");

      setTimeout(() => {
        navigate("/login");
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
            setError("Please check your input and try again.");
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
    <div className={styles.signupContainer}>
      <div className={styles.signupCard}>
        {/* Brand Section */}
        <div className={styles.brandSection}>
          <div className={styles.brandContent}>
            <span className={styles.badge}>TASK MANAGER</span>
            <h1>Organize Your Work. Track Your Progress. Get Things Done.</h1>
            <p>
              Manage your tasks, track progress, and stay organized with a simple
              and efficient task management workspace.
            </p>
          </div>
          <div className={styles.circleGraphic1}></div>
          <div className={styles.circleGraphic2}></div>
        </div>

        {/* Form Section */}
        <div className={styles.formSection}>
          <div className={styles.formHeader}>
            <h2>Create Account</h2>
            <p>Please enter your details to sign up.</p>
          </div>

          {error && <div className={styles.errorAlert}>{error}</div>}
          {success && <div className={styles.successAlert}>{success}</div>}

          <form onSubmit={handleSubmit} className={styles.form} noValidate>
            {/* Full Name */}
            <div className={styles.inputGroup}>
              <label htmlFor="full_name">Full Name</label>
              <input
                type="text"
                id="full_name"
                name="full_name"
                placeholder="Enter your full name"
                value={formData.full_name}
                onChange={handleChange}
              />
              {fieldErrors.full_name && (
                <span style={{ color: "#ef4444", fontSize: "12px", marginTop: "4px" }}>
                  {fieldErrors.full_name}
                </span>
              )}
            </div>

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
                <span style={{ color: "#ef4444", fontSize: "12px", marginTop: "4px" }}>
                  {fieldErrors.email}
                </span>
              )}
            </div>

            {/* Password */}
            <div className={styles.inputGroup}>
              <label htmlFor="password">Password</label>
              <div className={styles.passwordWrapper}>
                <input
                  type={showPassword ? "text" : "password"}
                  id="password"
                  name="password"
                  placeholder="At least 8 chars, 1 upper, 1 lower, 1 number"
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
                <span style={{ color: "#ef4444", fontSize: "12px", marginTop: "4px" }}>
                  {fieldErrors.password}
                </span>
              )}
            </div>

            {/* Confirm Password */}
            <div className={styles.inputGroup}>
              <label htmlFor="confirm_password">Confirm Password</label>
              <input
                type="password"
                id="confirm_password"
                name="confirm_password"
                placeholder="Re-enter your password"
                value={formData.confirm_password}
                onChange={handleChange}
              />
              {fieldErrors.confirm_password && (
                <span style={{ color: "#ef4444", fontSize: "12px", marginTop: "4px" }}>
                  {fieldErrors.confirm_password}
                </span>
              )}
            </div>

            {/* Submit */}
            <button type="submit" className={styles.submitBtn} disabled={loading}>
              {loading ? "Creating Account..." : "Sign Up"}
            </button>
          </form>

          {/* Navigation */}
          <div className={styles.footerLinks}>
            <p>
              Already have an account? <Link to="/login">Log in</Link>
            </p>

            <div className={styles.subLinks}>
              <Link to="/forgot-password">Forgot Password?</Link>
              <span>•</span>
              <Link to="/support">Need Help?</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;