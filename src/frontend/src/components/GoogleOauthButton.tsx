import { FunctionComponent } from "react";

const GoogleOauthButton: FunctionComponent = () => {
  return (
    <div className="self-stretch flex flex-row items-start justify-start z-[1] text-left text-mini text-darkslateblue-100 font-montserrat">
      <div className="self-stretch flex flex-row items-start justify-start gap-[10.699999999999932px]">
        <img
          className="h-[25.5px] w-[24.9px] relative"
          loading="lazy"
          alt=""
          src="/icons.svg"
        />
        <div className="flex flex-col items-start justify-start pt-[3.199999999999818px] px-0 pb-0">
          <div className="relative font-semibold">Continue with Google</div>
        </div>
      </div>
    </div>
  );
};

export default GoogleOauthButton;
