import { FunctionComponent, useMemo, type CSSProperties } from "react";

export type FrameComponent2Type = {
  decisionMakingProcess?: string;

  /** Style props */
  frameDivWidth?: CSSProperties["width"];
  // frameDivDebugCommit?: CSSProperties["debugCommit"];
  frameDivWidth1?: CSSProperties["width"];
  alliahLaneMinWidth?: CSSProperties["minWidth"];
  alliahLaneFlex?: CSSProperties["flex"];
  founderLayerioMinWidth?: CSSProperties["minWidth"];
  founderLayerioAlignSelf?: CSSProperties["alignSelf"];
  // groupIconDebugCommit?: CSSProperties["debugCommit"];
};

const FrameComponent2: FunctionComponent<FrameComponent2Type> = ({
  decisionMakingProcess,
  frameDivWidth,
  // frameDivDebugCommit,
  frameDivWidth1,
  alliahLaneMinWidth,
  alliahLaneFlex,
  founderLayerioMinWidth,
  founderLayerioAlignSelf,
  // groupIconDebugCommit,
}) => {
  const frameDivStyle: CSSProperties = useMemo(() => {
    return {
      width: frameDivWidth,
      // debugCommit: frameDivDebugCommit,
    };
  }, [frameDivWidth]);

  const frameDiv1Style: CSSProperties = useMemo(() => {
    return {
      width: frameDivWidth1,
    };
  }, [frameDivWidth1]);
  // , frameDivDebugCommit

  const alliahLaneStyle: CSSProperties = useMemo(() => {
    return {
      minWidth: alliahLaneMinWidth,
      flex: alliahLaneFlex,
    };
  }, [alliahLaneMinWidth, alliahLaneFlex]);

  const founderLayerioStyle: CSSProperties = useMemo(() => {
    return {
      minWidth: founderLayerioMinWidth,
      alignSelf: founderLayerioAlignSelf,
    };
  }, [founderLayerioMinWidth, founderLayerioAlignSelf]);

  // const groupIconStyle: CSSProperties = useMemo(() => {
  //   return {
  //     debugCommit: groupIconDebugCommit,
  //   };
  // }, [groupIconDebugCommit]);

  return (
    <div className="w-[495px]  items-start justify-start min-w-[400px] min-h-[700px] max-w-full text-left text-xl text-darkslateblue-100 font-montserrat lg:flex-1 lg:min-h-[auto] mq750:min-w-full">
      <div className="self-stretch  items-start justify-start gap-[35.5px] max-w-full mq750:gap-[18px_35.5px]">
        <div className="self-stretch h-[436px] flex flex-row items-start justify-start py-0 px-0.5 box-border max-w-full">
          <img
            className="h-[436px] flex-1 relative max-w-full "
            loading="lazy"
            alt=""
            src="/infographic-11@2x.png"
          />
        </div>
        <i className="self-stretch relative font-semibold mq450:text-base">
          <p className="[margin-block-start:0] [margin-block-end:11px]">
            KleeneStar.io revolutionized our advertising
          </p>
          <p className="[margin-block-start:0] [margin-block-end:11px]">
            approach. Its intuitive, real-time insights help
          </p>
          <p className="[margin-block-start:0] [margin-block-end:11px]">
            us understand our KPI and transform our
          </p>
          <p className="m-0 whitespace-pre-wrap">{decisionMakingProcess}</p>
        </i>
        <div className="self-stretch flex flex-row items-start justify-between gap-[20px] text-lg mq450:flex-wrap">
          <div
            className="flex flex-col items-start justify-start gap-[9px]"
            style={frameDivStyle}
          >
            <div
              className="flex flex-row items-start justify-start gap-[6px]"
              style={frameDiv1Style}
            >
              <div className="h-3   items-start justify-start pt-0 px-0 pb-0 box-border">
                {/* <img
                  className="w-3 h-0.5 relative"
                  loading="lazy"
                  alt=""
                  src="/rectangle-510.svg"
                /> */}
              </div>
              <div
                className="relative font-semibold inline-block min-w-[103px]"
                style={alliahLaneStyle}
              >
                Alliah Lane
              </div>
            </div>
            <div
              className="relative text-mini inline-block min-w-[129px]"
              style={founderLayerioStyle}
            >
              Founder, Layer.io
            </div>
          </div>
          <div className="h-[20.5px] w-[123.8px] flex flex-col items-start justify-start pt-[13px] px-0 pb-0 box-border">
            <img
              className="self-stretch h-[17.5px] relative max-w-full overflow-hidden shrink-0"
              loading="lazy"
              alt=""
              src="/group-2081.svg"
              // style={groupIconStyle}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default FrameComponent2;
