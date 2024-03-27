import { FunctionComponent } from "react";

const FrameComponent11: FunctionComponent = () => {
  return (
    <div className="flex-1 flex flex-col items-center justify-start pt-[200px] px-5 pb-[275px] box-border relative gap-[19px] min-w-[469px] max-w-full text-center text-11xl font-montserrat mq750:min-w-full mq450:pt-[115px] mq450:pb-[116px] mq450:box-border mq1050:pt-[177px] mq1050:pb-[179px] mq1050:box-border">
      <img
        className="w-full h-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full"
        alt=""
        src="/rectangle-506.svg"
      />
      <div className="w-[454px] flex flex-row items-start justify-center py-0 pr-0 pl-px box-border max-w-full text-left font-syne">
        <h1 className="m-0 relative text-inherit font-bold font-inherit whitespace-nowrap z-[1] mq750:text-5xl mq450:text-lg">
          Get Started
        </h1>
      </div>
      <div className="w-[554px] flex flex-col items-end justify-start pt-0 px-0 pb-5 box-border gap-[41px] max-w-full text-base mq450:gap-[20px_41px]">
        <div className="self-stretch flex flex-row items-start justify-end py-0 pr-3.5 pl-[15px] box-border max-w-full">
          <div className="flex-1 flex flex-col items-end justify-start gap-[5px] max-w-full">
            <div className="self-stretch relative z-[1]">{`A new way to run highly efficient marketing analytics `}</div>
            <div className="self-stretch flex flex-row items-start justify-end py-0 pr-[25.300000000000185px] pl-7">
              <div className="w-[554px] relative inline-block z-[1]">
                across channels and learn real-time insights 🚀
              </div>
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
            Create a workspace
          </button>
      </div>
      <div className="flex flex-row items-start justify-start py-0 px-[23px] box-border max-w-full text-sm">
        <div className="w-[408px] relative inline-block z-[1]">
          {`Already using KleeneStar? `}
          <span className="[text-decoration:underline]">
            Log in to an existing workspace
          </span>
        </div>
      </div>
    </div>
  );
};

export default FrameComponent11;
