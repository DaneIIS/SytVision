import GitHubIcon from "@mui/icons-material/GitHub";
import Link from "@mui/material/Link";
import Typography from "@mui/material/Typography";
import { styled, useTheme } from "@mui/material/styles";
import { useContext } from "react";
import { useLocation } from "react-router-dom";

import { ViseronContext } from "context/ViseronContext";

const Footer = styled("footer")(() => ({
  position: "relative",
  left: 0,
  bottom: 0,
  marginTop: "100px",
  paddingBottom: "35px",
}));

export default function AppFooter() {
  const theme = useTheme();
  const location = useLocation();
  const { version, gitCommit } = useContext(ViseronContext);
  const showFooter = !["/configuration", "/events", "/live"].includes(
    location.pathname,
  );

  return showFooter ? (
    <Footer>
      <Typography
        align="center"
        variant="subtitle2"
        color={theme.palette.text.secondary}
      >
        {/* 👇 renamed to SytVision */}
        SytVision - {version} - {gitCommit}
      </Typography>
      <Typography align="center" variant="subtitle2">
        <Link
          target="_blank"
          href="https://github.com/DaneIIS/SytVision"   // 👈 your repo
          color={theme.palette.text.secondary}
        >
          <GitHubIcon
            fontSize="small"
            sx={{
              verticalAlign: "middle",
              marginTop: "-3px",
              marginRight: "5px",
            }}
          />
          GitHub
        </Link>
      </Typography>
    </Footer>
  ) : null;
}
