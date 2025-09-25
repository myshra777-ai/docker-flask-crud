param(
    [string]$Name = "Rohit",
    [string]$Email = "rohit@example.com"
)

Write-Host "🚀 Starting CRUD test sequence with Name=$Name, Email=$Email..."

# 1. Add a user
Write-Host "`n👉 Adding user..."
$response = Invoke-WebRequest -Uri http://localhost:5000/add-user `
  -Method POST `
  -Body (@{name=$Name; email=$Email} | ConvertTo-Json) `
  -ContentType "application/json"
$response.Content | Write-Host

# 2. Get all users
Write-Host "`n👉 Fetching all users..."
(Invoke-WebRequest -Uri http://localhost:5000/get-users -Method GET).Content | Write-Host

# 3. Update the user
Write-Host "`n👉 Updating user with ID 1..."
$response = Invoke-WebRequest -Uri http://localhost:5000/update-user/1 `
  -Method PUT `
  -Body (@{name="$Name Updated"} | ConvertTo-Json) `
  -ContentType "application/json"
$response.Content | Write-Host

# 4. Get all users again
Write-Host "`n👉 Fetching all users after update..."
(Invoke-WebRequest -Uri http://localhost:5000/get-users -Method GET).Content | Write-Host

# 5. Delete the user
Write-Host "`n👉 Deleting user with ID 1..."
$response = Invoke-WebRequest -Uri http://localhost:5000/delete-user/1 -Method DELETE
$response.Content | Write-Host

# 6. Final check
Write-Host "`n👉 Final user list (should be empty)..."
(Invoke-WebRequest -Uri http://localhost:5000/get-users -Method GET).Content | Write-Host

Write-Host "`n✅ CRUD test sequence completed!"