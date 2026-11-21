import { useState } from "react";
import {
  Field,
  FieldGroup,
  FieldLabel,
  FieldSet,
  FieldError,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ApiError } from "@/api/helpers";
import { useLocation, Navigate } from "react-router-dom";
import { useAuth } from "@/hooks/use-auth";
import "./LoginPage.css";

function Login() {
  const location = useLocation();
  const from = location.state?.from?.pathname ?? "/devices";
  const { user, login } = useAuth();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: React.SyntheticEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const username = formData.get("username") as string;
    const password = formData.get("password") as string;
    setError(null);
    setSubmitting(true);
    try {
      await login(username, password);
    } catch (err) {
      setError(
        err instanceof ApiError && err.status === 401
          ? "Invalid username or password"
          : "Could not sign in. Please try again.",
      );
    } finally {
      setSubmitting(false);
    }
  }

  // Already logged in, or just logged in: go back to where the user came from.
  if (user) return <Navigate to={from} replace />;

  return (
    <div className="login-page">
      <div className="login-card">
        <h1 className="text-2xl font-bold mb-4">Sign in</h1>
        <form onSubmit={handleSubmit}>
          {/* <FieldSet className = "w-full max-w-xs"> */}
          <FieldSet>
            <FieldGroup>
              <Field>
                <FieldLabel htmlFor="username">Username</FieldLabel>
                <Input
                  id="username"
                  name="username"
                  placeholder="username"
                  type="text"
                  autoComplete="username"
                  required
                  maxLength={50}
                />
              </Field>
              <Field>
                <FieldLabel htmlFor="password">Password</FieldLabel>
                <Input
                  id="password"
                  name="password"
                  placeholder="********"
                  type="password"
                  autoComplete="current-password"
                  required
                  maxLength={50}
                />
              </Field>
            </FieldGroup>
          </FieldSet>
          {error && <FieldError>{error}</FieldError>}
          <div className="flex items-center justify-between mt-4">
            <Button type="submit" disabled={submitting}>
              Sign in
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Login;
