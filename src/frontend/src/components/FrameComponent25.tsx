import { FunctionComponent, useMemo, type CSSProperties } from "react";
import { useState } from 'react';

export type FrameComponent25Type = {
  googleAdsIsGooglesOnlineA?: string;
  platformAllowingBusinesse?: string;
  acrossVariousNetworks?: string;

  /** Style props */
  propWidth?: CSSProperties["width"];
  propWidth1?: CSSProperties["width"];
};

const FrameComponent25: FunctionComponent<FrameComponent25Type> = ({
  googleAdsIsGooglesOnlineA,
  platformAllowingBusinesse,
  acrossVariousNetworks,
  propWidth,
  propWidth1,
}) => {
  const googleAdsIsStyle: CSSProperties = useMemo(() => {
    return {
      width: propWidth,
    };
  }, [propWidth]);

  const acrossVariousNetworksStyle: CSSProperties = useMemo(() => {
    return {
      width: propWidth1,
    };
  }, [propWidth1]);
  const [isChecked, setIsChecked] = useState(false);

  const handleToggle = () => {
    setIsChecked(prev => !prev);
  };

  return (
    <div className="self-stretch flex flex-col items-start justify-start gap-[16.5px] max-w-full text-left text-mini text-darkslateblue-100 font-montserrat">
      <div className="w-[348.6px] flex flex-col items-start justify-start gap-[7.450000000000159px] max-w-full shrink-0">
        <div
          className="w-[327.4px] relative inline-block max-w-full z-[1]"
          style={googleAdsIsStyle}
        >
          {googleAdsIsGooglesOnlineA}
        </div>
        <div className="self-stretch relative z-[1]">
          {platformAllowingBusinesse}
        </div>
        <div
          className="w-[193.4px] relative inline-block z-[1]"
          style={acrossVariousNetworksStyle}
        >
          {acrossVariousNetworks}
        </div>
      </div>
      <img
        className="self-stretch h-[2.1px] relative max-w-full overflow-hidden shrink-0 z-[1]"
        loading="lazy"
        alt=""
        src="/path-28.svg"
      />
      <label className="cursor-pointer">
      <input
        type="checkbox"
        checked={isChecked}
        onChange={handleToggle}
        className="hidden"
      />
      <div className="relative">
        <div className={`w-[136px] h-[42.5px] bg-transparent absolute top-0 left-0 z-[1] ${isChecked ? 'bg-gray-300' : ''}`}></div>
        <div className="absolute top-[10.6px] left-[22.3px] text-mini font-montserrat text-darkslateblue-100 text-left inline-block w-[91.4px] h-[19.1px] min-w-[91.4px] z-[2]">
          Disconnect
        </div>
      </div>
    </label>
    </div>
  );
};

export default FrameComponent25;
