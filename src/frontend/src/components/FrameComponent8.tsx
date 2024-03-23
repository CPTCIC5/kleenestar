import { FunctionComponent, useMemo, type CSSProperties } from "react";

export type FrameComponent8Type = {
  unauthorizedEmail?: string;

  /** Style props */
  propAlignSelf?: CSSProperties["alignSelf"];
  propPadding?: CSSProperties["padding"];
  propWidth?: CSSProperties["width"];
  propMinWidth?: CSSProperties["minWidth"];
};

const FrameComponent8: FunctionComponent<FrameComponent8Type> = ({
  unauthorizedEmail,
  propAlignSelf,
  propPadding,
  propWidth,
  propMinWidth,
}) => {
  const frameDiv3Style: CSSProperties = useMemo(() => {
    return {
      alignSelf: propAlignSelf,
      padding: propPadding,
      width: propWidth,
    };
  }, [propAlignSelf, propPadding, propWidth]);

  const unauthorizedEmail1Style: CSSProperties = useMemo(() => {
    return {
      minWidth: propMinWidth,
    };
  }, [propMinWidth]);

  return (
    <div
      className="self-stretch flex flex-col items-start justify-start pt-0 px-0 pb-[5.099999999999909px] gap-[10.799999999999956px] text-left text-sm text-darkslateblue-100 font-montserrat"
      style={frameDiv3Style}
    >
      <div className="relative font-medium inline-block min-w-[46px] z-[1]">
        Email*
      </div>
      <div className="self-stretch flex flex-row items-start justify-start pt-[13.200000000000273px] px-[18.199999999999815px] pb-[13.799999999999727px] relative text-mini text-darkslateblue-200">
        <div className="relative z-[2]">@work-email.com</div>
        <div className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
          <img
            className="absolute h-full w-full top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full z-[1]"
            alt=""
            src="/rectangle-522.svg"
          />
          <img
            className="absolute top-[12.9px] left-[420.7px] w-[16.1px] h-[20.1px] z-[2]"
            alt=""
            src="/pen2svgrepocom.svg"
          />
        </div>
      </div>
      <div
        className="relative text-smi font-light text-orangered-300 inline-block min-w-[128px] z-[1]"
        style={unauthorizedEmail1Style}
      >
        {unauthorizedEmail}
      </div>
    </div>
  );
};

export default FrameComponent8;
