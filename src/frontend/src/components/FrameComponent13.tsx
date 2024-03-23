import { FunctionComponent, useMemo, type CSSProperties } from "react";

export type FrameComponent13Type = {
  newPassword?: string;
  password?: string;
  component627?: string;

  /** Style props */
  propPadding?: CSSProperties["padding"];
  propMinWidth?: CSSProperties["minWidth"];
  propMinWidth1?: CSSProperties["minWidth"];
};

const FrameComponent13: FunctionComponent<FrameComponent13Type> = ({
  newPassword,
  password,
  component627,
  propPadding,
  propMinWidth,
  propMinWidth1,
}) => {
  const frameDiv4Style: CSSProperties = useMemo(() => {
    return {
      padding: propPadding,
    };
  }, [propPadding]);

  const newPasswordStyle: CSSProperties = useMemo(() => {
    return {
      minWidth: propMinWidth,
    };
  }, [propMinWidth]);

  const passwordStyle: CSSProperties = useMemo(() => {
    return {
      minWidth: propMinWidth1,
    };
  }, [propMinWidth1]);

  return (
    <div
      className="self-stretch flex flex-col items-start justify-start pt-0 px-0 pb-[5.099999999999909px] gap-[10.300000000000182px] text-left text-sm text-darkslateblue-100 font-montserrat"
      style={frameDiv4Style}
    >
      <div
        className="relative font-medium inline-block min-w-[111px] z-[1]"
        style={newPasswordStyle}
      >
        {newPassword}
      </div>
      <div className="self-stretch flex flex-row items-start justify-start pt-[13.199999999999818px] px-[18.199999999999815px] pb-[13.800000000000182px] relative text-mini text-darkslateblue-200">
        <div
          className="relative inline-block min-w-[73px] z-[2]"
          style={passwordStyle}
        >
          {password}
        </div>
        <div className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
          <img
            className="absolute h-full w-full top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full z-[1]"
            alt=""
            src="/rectangle-522.svg"
          />
          <img
            className="absolute top-[14px] left-[418px] w-[21.5px] h-[19px] z-[2]"
            loading="lazy"
            alt=""
            src={component627}
          />
        </div>
      </div>
    </div>
  );
};

export default FrameComponent13;
