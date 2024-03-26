import { FunctionComponent, useMemo, type CSSProperties } from "react";

export type FrameComponent3Type = {
  /** Style props */
  // frameDivDebugCommit?: CSSProperties["debugCommit"];
  // propDebugCommit?: CSSProperties["debugCommit"];
};

const FrameComponent3: FunctionComponent<FrameComponent3Type> = ({
  // frameDivDebugCommit,
  // propDebugCommit,
}) => {
  // const frameDiv2Style: CSSProperties = useMemo(() => {
  //   return {
  //     debugCommit: frameDivDebugCommit,
  //   };
  // }, [frameDivDebugCommit]);

  // const groupIcon1Style: CSSProperties = useMemo(() => {
  //   return {
  //     debugCommit: propDebugCommit,
  //   };
  // }, [propDebugCommit]);

  return (
    <div className="w-[495px]  items-start justify-start min-w-[495px] min-h-[600px] max-w-full text-left text-xl text-darkslateblue-100 font-montserrat lg:flex-1 lg:min-h-[auto] mq750:min-w-full">
      <div className="self-stretch items-start justify-start gap-[35.5px] max-w-full mq750:gap-[18px_35.5px]">
        <div className="self-stretch h-[436px] flex flex-row items-start justify-start py-0 px-0.5 box-border max-w-full">
          <img
            className="h-[436px]  relative max-w-full overflow-hidden object-cover"
            loading="lazy"
            alt=""
            src="/infographic-11@2x.png"
          />
        </div>
        <h3 className="m-0 self-stretch relative text-inherit italic font-semibold font-inherit mq450:text-base">
          <p className="[margin-block-start:0] [margin-block-end:11px]">
            KleeneStar.io revolutionized our advertising
          </p>
          <p className="[margin-block-start:0] [margin-block-end:11px]">
            approach. Its intuitive, real-time insights help
          </p>
          <p className="[margin-block-start:0] [margin-block-end:11px]">
            us understand our KPI and transform our
          </p>
          <p className="m-0">decision-making process.</p>
        </h3>
        <div className="self-stretch flex flex-row items-start justify-between gap-[20px] text-lg mq450:flex-wrap">
          <div
            className="flex flex-col items-start justify-start gap-[9px]"
            // style={frameDiv2Style}
          >
            <div className="flex flex-row items-start justify-start gap-[6px]">
              <div className="h-3 flex  items-start justify-start pt-2.5 px-0 pb-0 box-border">
                <img
                  className="w-3 h-0.5 relative"
                  loading="lazy"
                  alt=""
                  src="/rectangle-510.svg"
                />
              </div>
              <div className="relative font-semibold inline-block min-w-[103px]">
                Alliah Lane
              </div>
            </div>
            <div className="relative text-mini inline-block min-w-[129px]">
              Founder, Layer.io
            </div>
          </div>
          <div className="h-[30.5px] w-[123.8px] flex flex-col items-start justify-start pt-[13px] px-0 pb-0 box-border">
            <img
              className="self-stretch h-[17.5px] relative max-w-full overflow-hidden shrink-0"
              loading="lazy"
              alt=""
              src="/group-2081.svg"
              // style={groupIcon1Style}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default FrameComponent3;
