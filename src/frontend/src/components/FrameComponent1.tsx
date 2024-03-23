import { FunctionComponent } from "react";

const FrameComponent11: FunctionComponent = () => {
  return (
    <div className="flex-1 flex flex-col items-center justify-start pt-[272px] px-5 pb-[275px] box-border relative gap-[19px] min-w-[469px] max-w-full text-center text-11xl text-darkslateblue-100 font-montserrat mq750:min-w-full mq450:pt-[115px] mq450:pb-[116px] mq450:box-border mq1050:pt-[177px] mq1050:pb-[179px] mq1050:box-border">
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
      <div className="w-[454px] flex flex-col items-end justify-start pt-0 px-0 pb-5 box-border gap-[41px] max-w-full text-base mq450:gap-[20px_41px]">
        <div className="self-stretch flex flex-row items-start justify-end py-0 pr-3.5 pl-[15px] box-border max-w-full">
          <div className="flex-1 flex flex-col items-end justify-start gap-[5px] max-w-full">
            <div className="self-stretch relative z-[1]">{`A new way to run highly efficient marketing analytics `}</div>
            <div className="self-stretch flex flex-row items-start justify-end py-0 pr-[25.300000000000185px] pl-7">
              <div className="w-[372px] relative inline-block z-[1]">
                across channels and learn real-time insights 🚀
              </div>
            </div>
          </div>
        </div>

        <button className="cursor-pointer pt-2.5 px-5 pb-3 bg-transparent self-stretch flex flex-row items-start justify-center relative mq450:pl-5 mq450:pr-5 mq450:box-border">
          <div className="relative text-mini font-semibold font-montserrat text-whitesmoke text-left z-2">
            Create a workspace
          </div>
          <div className="h-full w-full absolute top-0 right-0 bottom-0 left-0">
            <img
              className="absolute top-0 right-0 bottom-0 left-0 max-w-full max-h-full z-1"
              alt=""
              src="/rectangle-512.svg"
            />
            <img
              className="absolute top-13.5px left-302.1px w-16.8px h-3 z-2"
              alt=""
              src="/arrowrightsvgrepocom.svg"
            />
          </div>
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
