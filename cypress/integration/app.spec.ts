describe("Main Page", () => {
  before(() => {
    cy.visit("http://localhost:3000/");
  });
  it("Should contain links to all platforms", () => {
    cy.get('a[href*="linkedin"]');
    cy.get('a[href*="github"]');
    cy.get('a[href*="tryhackme"]');
  });
  it("Should be able to download resume", () => {
    cy.get('a[href*="Resume"]');
    cy.downloadFile(
      "http://localhost:3000/Resume.docx",
      "cypress/fixtures/Download",
      "Resume.docx"
    );
  });
});

export {};
