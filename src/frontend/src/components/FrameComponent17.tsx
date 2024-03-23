
import { useState } from 'react';
import { FunctionComponent, useMemo, type CSSProperties } from "react";


export type FrameComponent17Type = {
  googleAuthenticator?: string;
  useTheGoogleAuthenticator?: string;
  component665?: string;

  /** Style props */
  propWidth?: CSSProperties["width"];
};


const FrameComponent17: FunctionComponent<FrameComponent17Type> = ({
  googleAuthenticator,
  useTheGoogleAuthenticator,
  component665,
  propWidth,
}) => {
  const googleAuthenticatorStyle: CSSProperties = useMemo(() => {
    return {
      width: propWidth,
    };
  }, [propWidth]);
  const [isChecked, setIsChecked] = useState(false);

  const handleToggle = () => {
    setIsChecked((prev) => !prev);
  };
  

  return (
    <div className="self-stretch flex flex-col items-start justify-start pt-[25.5px] px-[27.300000000000185px] pb-[27.799999999999955px] box-border relative gap-[12.700000000000044px] max-w-full text-left text-lg text-darkslateblue-100 font-montserrat">
      <div
        className="w-[213.6px] relative font-semibold inline-block z-[1]"
        style={googleAuthenticatorStyle}
      >
        {googleAuthenticator}
      </div>
      <div className="w-[529.3px] relative text-sm inline-block max-w-full z-[1]">
        {useTheGoogleAuthenticator}
      </div>
      <div className="w-full h-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
        <img
          className="absolute h-full w-full top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full"
          alt=""
          src="/rectangle-646.svg"
        />
        <input
        type="checkbox"
        id="toggle"
        className="absolute top-[25px] left-[549.6px] z-[1] opacity-0"
        checked={isChecked}
        onChange={handleToggle}
        
      />
      <label
        htmlFor="toggle"
        className="absolute top-[25px] left-[549.6px] w-[51px] h-[25.5px] z-[1] cursor-pointer"
      >
        <div className="w-full h-full bg-gray-300 rounded-full"></div>
        {/* <div className={`absolute top-0 left-0 w-[25px] h-[25.5px] bg-white rounded-full transform ${isChecked ? 'translate-x-0' : 'translate-x-[26px]'} transition-transform duration-200 ease-in-out`}></div> */}
        <div className={`absolute top-0 left-0 w-[25px] h-[25.5px] bg-blue-500 rounded-full transform ${isChecked ? 'translate-x-[26px]' : 'translate-x-0'} transition-transform duration-200 ease-in-out`}></div>
      </label>
      </div>
    </div>
  );
};

export default FrameComponent17;
