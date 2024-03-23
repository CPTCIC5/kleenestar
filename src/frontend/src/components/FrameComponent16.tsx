import { FunctionComponent } from "react";
import FrameComponent17 from "./FrameComponent17";

const FrameComponent16: FunctionComponent = () => {
  return (
    <div className="flex-1 flex flex-col items-start justify-start gap-[37.700000000000045px] min-w-[409px] max-w-full text-left text-lg text-darkslateblue-100 font-montserrat lg:flex-1 mq750:gap-[19px_37.7px] mq750:min-w-full">
      <div className="self-stretch flex flex-col items-start justify-start pt-[25.5px] px-[27.800000000000185px] pb-[35.69999999999982px] box-border relative gap-[29.90000000000009px] max-w-full">
        <div className="w-[487.9px] flex flex-col items-start justify-start pt-0 px-0 pb-[13.700000000000044px] box-border gap-[12.700000000000044px] max-w-full">
          <div className="w-[178.6px] relative font-semibold inline-block z-[1]">
            Change Password
          </div>
          <div className="self-stretch relative text-sm z-[1]">
            Change your password will log you out of all devices and sessions.
          </div>
        </div>
        <div className="self-stretch flex flex-row items-start justify-start gap-[17.600000000000364px] text-sm mq750:flex-wrap">
          <div className="flex-1 flex flex-col items-start justify-start gap-[11px] min-w-[181px]">
            <div className="relative font-medium inline-block min-w-[111.6px] shrink-0 [debug_commit:f6aba90] z-[1]">
              New password
            </div>
            <div className="self-stretch flex flex-row items-start justify-start pt-3.5 px-[19.400000000000546px] pb-[14.700000000000044px] relative shrink-0 [debug_commit:f6aba90]">
              <input
                className="w-[118px] [border:none] [outline:none] font-montserrat text-mini bg-[transparent] h-[19.1px] relative text-darkslateblue-200 text-left inline-block p-0 z-[2]"
                placeholder="New password"
                type="text"
              />
              <div className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
                <img
                  className="absolute h-full w-full top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full z-[1]"
                  alt=""
                  src="/rectangle-522.svg"
                />
                <img
                  className="absolute top-[13.7px] left-[242.8px] w-[17.1px] h-[21.3px] z-[2]"
                  alt=""
                  src="/pen2svgrepocom.svg"
                />
              </div>
            </div>
          </div>
          <div className="flex-1 flex flex-col items-start justify-start gap-[11.350000000000025px] min-w-[181px]">
            <div className="relative font-medium z-[1]">Confirm password</div>
            <div className="self-stretch flex flex-row items-start justify-start pt-3.5 px-[19.399999999999636px] pb-[14.700000000000044px] relative text-mini text-darkslateblue-200">
              {/* <div className="relative z-[2]">Cornfirm password</div> */}
              <div className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
              <input
                className="w-[118px] [border:none] [outline:none] font-montserrat text-mini bg-[transparent] h-[19.1px] relative text-darkslateblue-200 text-left inline-block p-0 z-[2]"
                placeholder="Confirm password"
                type="text"
              />
              <div className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
                
                <img
                  className="absolute top-[13.7px] left-[242.8px] w-[17.1px] h-[21.3px] z-[2]"
                  alt=""
                  src="/pen2svgrepocom.svg"
                />
              </div>
              </div>
            </div>
            <div className="w-[224.3px] relative text-smi text-royalblue inline-block z-[1]">
              Password confirmation matches
            </div>
          </div>
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
            Change Password
          </button>
        <div className="w-full h-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
          {/* <img
            className="absolute h-full w-[calc(100%_-_1px)] top-[0px] right-[0.5px] bottom-[0px] left-[0.5px] max-w-full overflow-hidden max-h-full"
            alt=""
            src="/rectangle-645.svg"
          /> */}
          <img
            className="absolute top-[102px] left-[0px] w-[629.3px] h-px z-[1]"
            alt=""
            src="/line-107.svg"
          />
          <img
            className="absolute top-[213.1px] left-[28.2px] w-[177.5px] h-[11.7px] z-[1]"
            loading="lazy"
            alt=""
            src="/group-2139.svg"
          />
        </div>
      </div>
      <FrameComponent17
        googleAuthenticator="Google Authenticator"
        useTheGoogleAuthenticator="Use the Google Authenticator app to generate one time security codes."
        component665="/component-6--65.svg"
      />
      <FrameComponent17
        googleAuthenticator="Two Factor Authentication"
        useTheGoogleAuthenticator="Require a second authentication method in addition to your password."
        component665="/component-6--66.svg"
        propWidth="263.6px"
      />
    </div>
  );
};

export default FrameComponent16;
