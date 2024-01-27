import {
  MDBCard,
  MDBCardBody,
  MDBCardTitle,
  MDBCardText,
  MDBCardImage,
} from "mdb-react-ui-kit";

import styles from "./projects.module.css";
export default function projects() {
  return (
    <>
      <h1 style={{ textAlign: "center" }}>Projects</h1>
      <div className={styles.projects}>
        <div className={styles.card}>
          <MDBCard>
            <MDBCardImage
              style={{
                borderTopRightRadius: "25px",
                borderTopLeftRadius: "25px",
              }}
              src="https://user-images.githubusercontent.com/29875928/189706365-64882191-53b9-469e-a7d3-7709c2f60df0.gif"
              position="top"
            />
            <MDBCardBody>
              <MDBCardTitle>
                <a href="https://github.com/misaelaguayo/Rust-packet-visualizer">
                  Rust Packet Visualization
                </a>
              </MDBCardTitle>
              <MDBCardText>
                A packet for visualizing network requests
              </MDBCardText>
            </MDBCardBody>
          </MDBCard>
        </div>
        <div className={styles.card}>
          <a href="https://github.com/misaelaguayo/markdown-preview-haskell">
            Preview markdown in terminal
          </a>
        </div>
      </div>
    </>
  );
}
