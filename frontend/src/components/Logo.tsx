import teamUpLogo from "../assets/images/teamUpLogo.png";
import "../styles/Logo.css";

const Logo = () => {
  return (
    <div>
      <img src={teamUpLogo} className="logo" alt="Team Up logo" />
    </div>
  );
};
export default Logo;
