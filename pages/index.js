import Head from 'next/head'
import Layout, { siteTitle } from '../components/layout'
import utilStyles from '../styles/utils.module.css'

export default function Home() {
  return (
    <Layout home>
      <Head>
        <title>{siteTitle}</title>
      </Head>
      <section className={utilStyles.headingMd}>
        <p>I am a software engineer interested in information security. Some more of my interests include low level networking, reverse engineering, and virtual machine languages</p>
        <p>
          This blog will be used to document some of the CTFs I participate and some of my interests.{' '}
          <a href="https://www.linkedin.com/in/misael-aguayo-58b22985">LinkedIn</a>
        </p>
      </section>
    </Layout>
  )
}
