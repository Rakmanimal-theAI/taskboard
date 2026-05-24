import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { register } from '../api/auth'

const RegisterPage = () => {
    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState<string | null>(null)
    const [loading, setLoading] = useState(false)

    const navigate = useNavigate()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()  // stops the page from refreshing
        setLoading(true)
        setError(null)
        try {
            await register({ name, email, password })
            navigate('/login')
        } catch (err) {
            setError('Invalid name, email or password')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div>
          <h1>Sign Up</h1>
          <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Name"
            />
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
            />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
            />
            {error && <p>{error}</p>}
            <button type="submit" disabled={loading}>
              {loading ? 'Signing up...' : 'Sign up'}
            </button>
          </form>
          <p className="text-sm text-center text-gray-500">
            Already have an account?{' '}
            <span
              onClick={() => navigate('/login')}
              className="text-blue-600 cursor-pointer hover:underline"
            >
              Log in
            </span>
          </p>
        </div>
    )
}

export default RegisterPage
