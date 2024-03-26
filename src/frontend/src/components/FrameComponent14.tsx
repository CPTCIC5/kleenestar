import { FunctionComponent } from "react";

const FrameComponent14: FunctionComponent = () => {
  return (
    <div className="w-[722px] flex flex-col items-center justify-start pt-[63.19999999999982px] px-5 pb-[64.79999999999973px] box-border relative gap-[374.6000000000003px] max-w-full text-left text-11xl text-darkslateblue-100 font-syne mq675:gap-[187px_374.6px] mq675:pt-[41px] mq675:pb-[42px] mq675:box-border">
      <div className="w-[454px] flex flex-row items-start justify-start py-0 pr-[35px] pl-[33px] box-border max-w-full">
        <div className="flex-1 flex flex-col items-start justify-start gap-[19px] max-w-full">
          <div className="flex flex-row items-start justify-start py-0 pr-[54px] pl-[57.5px] mq450:pl-5 mq450:pr-5 mq450:box-border">
            <h1 className="m-0 relative text-inherit font-bold font-inherit z-[1] mq450:text-lg mq750:text-5xl">
              Password Saved
            </h1>
          </div>
          <div className="self-stretch relative text-base font-montserrat text-center z-[1]">
            Your password has been successfuly updated. 🥳
          </div>
        </div>
      </div>
      
      <div className="w-full h-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
        <img
          className="absolute top-[181.8px] left-[195px] w-[331.9px] h-[289.5px] z-[1]"
          loading="lazy"
          alt=""
          src="/access-login--unlock-illustration.svg"
        />
      </div>
      <button
            className="cursor-pointer"
            style={{
              backgroundColor: "#1C274C",
              color: "white",
              borderRadius: "10px",
              width: "100%", // Set width to 100% for responsiveness
              height: "40px",
              flexShrink: 0,
              border: "none", // If you want to remove the border
              padding: 0, // If you want to remove padding
              alignSelf: "stretch", // If you want the button to stretch vertically
              position: "relative", // If you want to position child elements absolutely
              maxWidth: "454px", // Set maximum width for larger screens
              margin: "0 auto", // Center the button horizontally
            }}
          >
            Go to Login
          </button>
    </div>
  );
};

export default FrameComponent14;
