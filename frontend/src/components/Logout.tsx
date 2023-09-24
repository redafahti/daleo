// A component that renders the logout button
const Logout = ({ logout }: { logout: () => void }) => {
  // Return a JSX element that renders the logout button
  return (
    <div className="logout">
      <button onClick={logout}>Logout</button>
    </div>
  );
};

export default Logout;
