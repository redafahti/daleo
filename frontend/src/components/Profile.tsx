import { UsersService } from "../client";

// A component that renders the user profile
const Profile = async () => {
  // Make a GET request to the me endpoint
  const response = await UsersService.usersGetMyUserProfile();
  // Get the username from the response data
  const username = response.username;
  // Return a JSX element that renders the user profile
  return (
    <div className="profile">
      <h2>Profile</h2>
      <p>Username: {username}</p>
    </div>
  );
};

export default Profile;
