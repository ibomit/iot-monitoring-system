export class ApiError extends Error {
    status: number

    constructor(message: string, status: number) {
        super(message)
        this.name = 'ApiError'
        this.status = status
    }
}

// Turns a failed response into an ApiError. Uses the backend's "detail"
// message when it is a string (validation errors send a list, so they get the fallback).
export async function toApiError(
    response: Response,
    fallback: string
): Promise<ApiError> {
    const errorData = await response.json().catch(() => null)
    const message =
        typeof errorData?.detail === 'string' ? errorData.detail : fallback

    return new ApiError(message, response.status)
}
