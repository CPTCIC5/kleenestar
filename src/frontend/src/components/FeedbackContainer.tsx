import { FunctionComponent, useMemo, type CSSProperties } from "react";

export type FeedbackContainerType = {
  askMeAnything?: string;
  group1965?: string;

  /** Style props */
  propAlignSelf?: CSSProperties["alignSelf"];
  propWidth?: CSSProperties["width"];
  // propDebugCommit?: CSSProperties["debugCommit"];
  // propDebugCommit1?: CSSProperties["debugCommit"];
  propMinWidth?: CSSProperties["minWidth"];
};

const FeedbackContainer: FunctionComponent<FeedbackContainerType> = ({
  askMeAnything,
  group1965,
  propAlignSelf,
  propWidth,
  // propDebugCommit,
  // propDebugCommit1,
  propMinWidth,
}) => {
  const feedbackContainerStyle: CSSProperties = useMemo(() => {
    return {
      alignSelf: propAlignSelf,
      width: propWidth,
    };
  }, [propAlignSelf, propWidth]);

  // const gallerySendSvgrepoComIconStyle: CSSProperties = useMemo(() => {
  //   return {
  //     debugCommit: propDebugCommit,
  //   };
  // }, [propDebugCommit]);

  // const askMeAnythingStyle: CSSProperties = useMemo(() => {
  //   return {
  //     debugCommit: propDebugCommit1,
  //     minWidth: propMinWidth,
  //   };
  // }, [propDebugCommit1, propMinWidth]);

  return (
    <div
      className="self-stretch flex flex-col items-start justify-start gap-[16.299999999999727px] max-w-full text-left text-base text-darkslateblue-200 font-montserrat"
      style={feedbackContainerStyle}
    >
      <div className="self-stretch flex flex-row items-end justify-between pt-[5.900000000000091px] pb-1.5 pr-[7px] pl-[26.699999999999815px] relative shrink-0 [debug_commit:f6aba90] z-[1] mq450:flex-wrap">
        <img
          className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full"
          alt=""
          src="/rectangle-2.svg"
        />
        <div className="h-[33.7px] flex flex-col items-start justify-end pt-0 px-0 pb-[8.800000000000182px] box-border">
          <div className="flex-1 flex flex-row items-start justify-start gap-[25.30000000000109px]">
            <img
              className="h-[24.9px] w-[24.9px] relative min-h-[25px] shrink-0 [debug_commit:f6aba90] z-[1]"
              loading="lazy"
              alt=""
              src="/gallerysendsvgrepocom2.svg"
              // style={gallerySendSvgrepoComIconStyle}
            />
            <div className="flex flex-col items-start justify-start pt-[1.900000000000091px] px-0 pb-0">
              <div
                className="relative shrink-0 [debug_commit:f6aba90] z-[1]"
                // style={askMeAnythingStyle}
              >
                {askMeAnything}
              </div>
            </div>
          </div>
        </div>
        <div className="h-[42.6px] w-[41.8px] relative z-[2] flex items-center justify-center">
          <img
            className="h-full w-full z-[2] object-contain absolute left-[0px] top-[3px] [transform:scale(1.718)]"
            loading="lazy"
            alt=""
            src={group1965}
          />
        </div>
      </div>
      <div className="self-stretch flex flex-row items-start justify-center py-0 pr-[27px] pl-5 box-border max-w-full text-xs text-darkslateblue-100">
        <div className="w-[464.9px] relative inline-block shrink-0 [debug_commit:f6aba90] z-[1]">
          KleeneStar can make mistakes. Consider checking important information.
        </div>
      </div>
    </div>
  );
};

export default FeedbackContainer;
