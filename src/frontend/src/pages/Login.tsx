import { FunctionComponent } from "react";
import FrameComponent from "../components/FrameComponent";

const Login: FunctionComponent = () => {
  return (
    <div className="flex flex-row items-start justify-center w-full">        
      <div className="w-full max-w-[25%] flex items-end justify-middle">
        <FrameComponent />
      </div>
    </div>
  );
};

export default Login;
